"""
oi_runtime_v0_1.py - Hardware Attestation, Speed-of-Light RTT & Tier 0 Promotion Subsystem
Author: Kara Faith Sypen
Architecture: ERA-GOS / LucidFluence / Observer Intelligence (OI) Runtime
"""

import time
import math
import hmac
import hashlib
import secrets
import json
from typing import Dict, Any, Tuple, Optional, List, Set
from dataclasses import dataclass, asdict
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, ec, rsa, ed25519
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature

# Physical constants
SPEED_OF_LIGHT_VACUUM_MPS = 299_792_458.0
FIBER_PROPAGATION_FACTOR = 0.670
EFFECTIVE_PROPAGATION_SPEED_MPS = SPEED_OF_LIGHT_VACUUM_MPS * FIBER_PROPAGATION_FACTOR


@dataclass(frozen=True)
class GeoCoordinates:
    latitude: float
    longitude: float
    elevation_m: float


@dataclass(frozen=True)
class TPM20Quote:
    pcr_digest: bytes           # Composite SHA-256 hash of PCR banks (PCR 0-7, 14)
    pcr_mask: int               # Bitmask of included PCR registers
    quote_signature: bytes      # AIK signature over TPMS_ATTEST
    attestation_data: bytes     # Raw serialized TPMS_ATTEST blob containing nonce + PCR digest
    aik_public_key_pem: bytes   # Public key of registered TPM AIK


@dataclass(frozen=True)
class PhysicalChallengePacket:
    nonce: bytes                # High-entropy, single-use 256-bit challenge
    timestamp_sent_ns: int      # Monotonic hardware clock timestamp (nanoseconds)
    target_node_id: str
    target_coordinates: GeoCoordinates


@dataclass(frozen=True)
class AuthorityTokenPayload:
    token_id: str
    issuer_entity: str
    target_scope: str
    created_at_epoch: int
    expires_at_epoch: int
    single_use_nonce: str
    required_quorum_nodes: List[str]
    system_architecture: str


@dataclass(frozen=True)
class AuthorityToken:
    payload: AuthorityTokenPayload
    signature_bytes: bytes
    issuer_public_key_pem: bytes


class HardwareAttestationEngine:
    """Enforces unforgeable physical grounding via TPM 2.0 quotes and speed-of-light RTT."""

    def __init__(self, allowed_pcr_digests: Dict[str, bytes], max_processing_jitter_ms: float = 4.5):
        self.allowed_pcr_digests = allowed_pcr_digests
        self.max_processing_jitter_sec = max_processing_jitter_ms / 1000.0
        self.consumed_nonces: Set[bytes] = set()

    def generate_proximity_challenge(self, target_node_id: str, coords: GeoCoordinates) -> PhysicalChallengePacket:
        return PhysicalChallengePacket(
            nonce=secrets.token_bytes(32),
            timestamp_sent_ns=time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW),
            target_node_id=target_node_id,
            target_coordinates=coords
        )

    def verify_tpm2_quote(self, quote: TPM20Quote, challenge_nonce: bytes, expected_node_id: str) -> Tuple[bool, str]:
        if challenge_nonce not in quote.attestation_data:
            return False, "REJECTED: Challenge nonce absent in attestation data."

        if challenge_nonce in self.consumed_nonces:
            return False, "REJECTED: Challenge nonce has already been consumed."
        self.consumed_nonces.add(challenge_nonce)

        try:
            public_key = load_pem_public_key(quote.aik_public_key_pem)
            if isinstance(public_key, rsa.RSAPublicKey):
                public_key.verify(quote.quote_signature, quote.attestation_data, padding.PKCS1v15(), hashes.SHA256())
            elif isinstance(public_key, ec.EllipticCurvePublicKey):
                public_key.verify(quote.quote_signature, quote.attestation_data, ec.ECDSA(hashes.SHA256()))
            else:
                return False, "REJECTED: Unsupported AIK key type."
        except InvalidSignature:
            return False, "REJECTED: Cryptographic AIK signature verification failed on TPM quote."
        except Exception as e:
            return False, f"REJECTED: Failed to parse AIK: {str(e)}"

        golden_digest = self.allowed_pcr_digests.get(expected_node_id)
        if not golden_digest:
            return False, f"REJECTED: No trusted PCR baseline profile found for node '{expected_node_id}'."

        if not hmac.compare_digest(quote.pcr_digest, golden_digest):
            return False, "REJECTED: TPM PCR state mismatch (possible hypervisor or altered kernel)."

        return True, "TPM 2.0 Hardware Quote Validated: Bare-Metal Root of Trust Verified."

    @staticmethod
    def calculate_great_circle_distance_m(loc1: GeoCoordinates, loc2: GeoCoordinates) -> float:
        earth_radius_m = 6_371_000.0
        phi1 = math.radians(loc1.latitude)
        phi2 = math.radians(loc2.latitude)
        delta_phi = math.radians(loc2.latitude - loc1.latitude)
        delta_lambda = math.radians(loc2.longitude - loc1.longitude)

        a = math.sin(delta_phi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0)**2)
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        surface_dist = earth_radius_m * c
        delta_elevation = loc2.elevation_m - loc1.elevation_m
        return math.sqrt(surface_dist**2 + delta_elevation**2)

    def verify_speed_of_light_rtt(
        self,
        challenge: PhysicalChallengePacket,
        verifier_coords: GeoCoordinates,
        timestamp_recv_ns: int
    ) -> Tuple[bool, str, float]:
        elapsed_ns = timestamp_recv_ns - challenge.timestamp_sent_ns
        if elapsed_ns <= 0:
            return False, "REJECTED: Clock inversion or non-monotonic timing detected.", 0.0

        elapsed_sec = elapsed_ns / 1_000_000_000.0
        straight_line_dist_m = self.calculate_great_circle_distance_m(verifier_coords, challenge.target_coordinates)
        min_physics_rtt_sec = (2.0 * straight_line_dist_m) / EFFECTIVE_PROPAGATION_SPEED_MPS
        max_allowable_rtt_sec = min_physics_rtt_sec + self.max_processing_jitter_sec

        if elapsed_sec < min_physics_rtt_sec * 0.95:
            return False, f"REJECTED: Superluminal anomaly ({elapsed_sec * 1000:.3f} ms). Coordinates false.", elapsed_sec

        if elapsed_sec > max_allowable_rtt_sec:
            excess_ms = (elapsed_sec - max_allowable_rtt_sec) * 1000.0
            return False, f"REJECTED: Propagation delay exceeded by {excess_ms:.2f} ms (Proxy/Relay detected).", elapsed_sec

        return True, f"Physical Grounding Confirmed (RTT: {elapsed_sec * 1000:.3f} ms).", elapsed_sec


class AuthorityTokenIssuer:
    """Issues single-use AuthorityTokens signed by Kara Faith Sypen."""
    EXPECTED_SOVEREIGN_ENTITY = "Kara Faith Sypen"
    TARGET_SCOPE = "scope:transition:tier0_egress"
    SYSTEM_ARCH = "ERA-GOS / LucidFluence / OI-v0.2.1"
    NEO_QUORUM_NODES = [
        "CLE-WESTLAKE-01",
        "CLE-VALLEYVIEW-02",
        "CLE-METROHEALTH-03",
        "EAST-LAKE-04",
        "SOUTH-AKRON-CANTON-05"
    ]

    def __init__(self, private_key: ed25519.Ed25519PrivateKey):
        self._private_key = private_key
        self._public_key = private_key.public_key()

    def generate_tier0_egress_token(self, validity_window_sec: int = 300) -> AuthorityToken:
        now = int(time.time())
        payload = AuthorityTokenPayload(
            token_id=f"AUTH-T0-EGR-{secrets.token_hex(6).upper()}",
            issuer_entity=self.EXPECTED_SOVEREIGN_ENTITY,
            target_scope=self.TARGET_SCOPE,
            created_at_epoch=now,
            expires_at_epoch=now + validity_window_sec,
            single_use_nonce=secrets.token_hex(32),
            required_quorum_nodes=self.NEO_QUORUM_NODES,
            system_architecture=self.SYSTEM_ARCH
        )
        canonical_bytes = json.dumps(asdict(payload), sort_keys=True).encode("utf-8")
        signature = self._private_key.sign(canonical_bytes)
        pub_pem = self._public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return AuthorityToken(payload=payload, signature_bytes=signature, issuer_public_key_pem=pub_pem)


class Tier0PromotionController:
    """Evaluates the 4 deterministic promotion gates for Tier 0 release."""

    def __init__(self, authorized_sovereign_pubkey_pem: bytes):
        self.authorized_pubkey_pem = authorized_sovereign_pubkey_pem
        self.consumed_token_ids: Set[str] = set()
        self.consumed_nonces: Set[str] = set()
        self.current_tier0_state = "ISOLATED_NOMINAL"

    def _verify_cryptographic_token(self, token: AuthorityToken) -> Tuple[bool, str]:
        payload = token.payload
        if payload.token_id in self.consumed_token_ids:
            return False, f"REJECTED: AuthorityToken '{payload.token_id}' already consumed."
        if payload.single_use_nonce in self.consumed_nonces:
            return False, f"REJECTED: Nonce '{payload.single_use_nonce}' already burned."
        if payload.target_scope != "scope:transition:tier0_egress":
            return False, f"REJECTED: Unauthorized scope '{payload.target_scope}'."
        if payload.issuer_entity != "Kara Faith Sypen":
            return False, f"REJECTED: Unauthorized issuer '{payload.issuer_entity}'."

        now = int(time.time())
        if now < payload.created_at_epoch or now > payload.expires_at_epoch:
            return False, "REJECTED: Token expired or timestamp invalid."

        if token.issuer_public_key_pem.strip() != self.authorized_pubkey_pem.strip():
            return False, "REJECTED: Sovereign public key mismatch."

        try:
            pubkey = serialization.load_pem_public_key(token.issuer_public_key_pem)
            if not isinstance(pubkey, ed25519.Ed25519PublicKey):
                return False, "REJECTED: Key must be ed25519."
            canonical_bytes = json.dumps(asdict(payload), sort_keys=True).encode("utf-8")
            pubkey.verify(token.signature_bytes, canonical_bytes)
        except InvalidSignature:
            return False, "REJECTED: Cryptographic signature verification failed."
        except Exception as e:
            return False, f"REJECTED: Token error: {str(e)}"

        return True, "AuthorityToken verified."

    def execute_tier0_egress_transition(
        self,
        token: AuthorityToken,
        tpm_corridor_attestation_results: Dict[str, bool],
        grok_attack_002_passed: bool,
        substation_variance_pct: float,
        safe_harbor_violations: int
    ) -> Dict[str, Any]:
        token_valid, token_msg = self._verify_cryptographic_token(token)
        if not token_valid:
            return {"status": "PROMOTION_DENIED", "gate_failed": "GATE_4_SOVEREIGN_RELEASE", "reason": token_msg}

        if not grok_attack_002_passed:
            return {"status": "PROMOTION_DENIED", "gate_failed": "GATE_1_ADVERSARIAL_MATRIX", "reason": "GROK-ATTACK-002 suite not cleared."}

        missing_nodes = [n for n in token.payload.required_quorum_nodes if not tpm_corridor_attestation_results.get(n, False)]
        if missing_nodes:
            return {"status": "PROMOTION_DENIED", "gate_failed": "GATE_2_CORRIDOR_TPM_QUORUM", "reason": f"Missing TPM quotes: {missing_nodes}"}

        if abs(substation_variance_pct) > 0.2:
            return {"status": "PROMOTION_DENIED", "gate_failed": "GATE_3_GVP_DAMPING", "reason": f"Variance {substation_variance_pct}% exceeds +/-0.2%."}

        if safe_harbor_violations > 0:
            return {"status": "PROMOTION_DENIED", "gate_failed": "GATE_3_SAFE_HARBOR_DECOUPLING", "reason": "Safe-harbor breach detected."}

        self.consumed_token_ids.add(token.payload.token_id)
        self.consumed_nonces.add(token.payload.single_use_nonce)
        self.current_tier0_state = "PRODUCTION_ROOT_ANCHOR"

        return {
            "status": "PROMOTION_SUCCESSFUL",
            "tier0_state": self.current_tier0_state,
            "egress_enabled": True,
            "token_id_consumed": token.payload.token_id,
            "quorums_satisfied": token.payload.required_quorum_nodes,
            "promoted_at_epoch": int(time.time()),
            "message": "Tier 0 successfully transitioned out of loopback. Egress into Tier 1 peer mesh activated."
        }
