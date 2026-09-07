from __future__ import annotations

import base64
import hashlib
import json
import time
import uuid
from dataclasses import asdict, dataclass
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)


SCHEME = "ED25519_V1"
ENROLLMENT_VERSION = "AETHERIS_NODE_ENROLLMENT_V1"


class EnrollmentError(ValueError):
    pass


@dataclass(frozen=True)
class IdentityPublic:
    did: str
    public_key_hex: str
    scheme: str = SCHEME


@dataclass(frozen=True)
class NodeEnrollment:
    version: str
    root_did: str
    root_public_key: str
    node_did: str
    node_public_key: str
    scopes: tuple[str, ...]
    nonce: str
    issued_at: int
    expires_at: int
    external_delivery_enabled: bool


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _derive_private_key(seed_material: bytes) -> Ed25519PrivateKey:
    if not isinstance(seed_material, bytes) or not seed_material:
        raise EnrollmentError("seed material must be non-empty bytes")
    seed = hashlib.sha256(seed_material).digest()
    return Ed25519PrivateKey.from_private_bytes(seed)


def _public_bytes_hex(private_key: Ed25519PrivateKey) -> str:
    return private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()


def _did(role: str, public_key_hex: str) -> str:
    return f"did:era:{role}:{public_key_hex}"


class RootAuthority:
    def __init__(self, seed_material: bytes):
        self._private_key = _derive_private_key(seed_material)
        self.public_key_hex = _public_bytes_hex(self._private_key)
        self.did = _did("root", self.public_key_hex)

    @property
    def public_identity(self) -> IdentityPublic:
        return IdentityPublic(self.did, self.public_key_hex)

    def sign(self, payload: bytes) -> str:
        return "ed25519:" + base64.b64encode(
            self._private_key.sign(payload)
        ).decode("ascii")


class OperationalNode:
    def __init__(self, seed_material: bytes):
        self._private_key = _derive_private_key(seed_material)
        self.public_key_hex = _public_bytes_hex(self._private_key)
        self.did = _did("aetheris", self.public_key_hex)

    @property
    def public_identity(self) -> IdentityPublic:
        return IdentityPublic(self.did, self.public_key_hex)


def create_node_enrollment(
    root: RootAuthority,
    node: OperationalNode,
    *,
    scopes: tuple[str, ...] = ("LOCAL_LEDGER", "SIGN_BLOCKS", "DRY_RUN_AUTHORIZATION"),
    ttl_seconds: int = 86400,
) -> dict[str, Any]:
    if ttl_seconds <= 0:
        raise EnrollmentError("ttl_seconds must be positive")

    now = int(time.time())
    enrollment = NodeEnrollment(
        version=ENROLLMENT_VERSION,
        root_did=root.did,
        root_public_key=root.public_key_hex,
        node_did=node.did,
        node_public_key=node.public_key_hex,
        scopes=tuple(sorted(set(scopes))),
        nonce=str(uuid.uuid4()),
        issued_at=now,
        expires_at=now + ttl_seconds,
        external_delivery_enabled=False,
    )
    payload = asdict(enrollment)
    canonical = _canonical_json(payload)
    return {
        "enrollment": payload,
        "enrollment_id": hashlib.sha256(canonical).hexdigest(),
        "signature_scheme": SCHEME,
        "root_signature": root.sign(canonical),
    }


def verify_node_enrollment(packet: dict[str, Any], *, now: int | None = None) -> tuple[bool, str]:
    try:
        if packet.get("signature_scheme") != SCHEME:
            return False, "UNSUPPORTED_SIGNATURE_SCHEME"

        enrollment = packet["enrollment"]
        if enrollment.get("version") != ENROLLMENT_VERSION:
            return False, "UNSUPPORTED_ENROLLMENT_VERSION"
        if enrollment.get("external_delivery_enabled") is not False:
            return False, "EXTERNAL_DELIVERY_MUST_BE_DISABLED"

        current = int(time.time()) if now is None else now
        issued_at = int(enrollment["issued_at"])
        expires_at = int(enrollment["expires_at"])
        if issued_at > current + 30:
            return False, "ISSUED_AT_IN_FUTURE"
        if expires_at <= current:
            return False, "ENROLLMENT_EXPIRED"

        root_public_key_hex = enrollment["root_public_key"]
        expected_root_did = _did("root", root_public_key_hex)
        if enrollment.get("root_did") != expected_root_did:
            return False, "ROOT_DID_KEY_MISMATCH"

        node_public_key_hex = enrollment["node_public_key"]
        expected_node_did = _did("aetheris", node_public_key_hex)
        if enrollment.get("node_did") != expected_node_did:
            return False, "NODE_DID_KEY_MISMATCH"

        canonical = _canonical_json(enrollment)
        expected_id = hashlib.sha256(canonical).hexdigest()
        if packet.get("enrollment_id") != expected_id:
            return False, "ENROLLMENT_ID_MISMATCH"

        signature = packet.get("root_signature", "")
        if not signature.startswith("ed25519:"):
            return False, "MALFORMED_ROOT_SIGNATURE"
        raw_signature = base64.b64decode(signature.removeprefix("ed25519:"), validate=True)

        public_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(root_public_key_hex))
        public_key.verify(raw_signature, canonical)
        return True, "ROOT_AUTHORITY_VERIFIED"

    except InvalidSignature:
        return False, "INVALID_ROOT_SIGNATURE"
    except (KeyError, TypeError, ValueError, base64.binascii.Error):
        return False, "MALFORMED_ENROLLMENT"
