"""
tests/test_hardware_attestation.py - Pytest Suite for TPM 2.0 & Tier 0 Promotion
Target: oi_runtime_v0_1.py
"""

import pytest
import secrets
import hashlib
from typing import Tuple
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding, ed25519

from oi_runtime_v0_1 import (
    HardwareAttestationEngine,
    GeoCoordinates,
    TPM20Quote,
    PhysicalChallengePacket,
    AuthorityTokenIssuer,
    Tier0PromotionController,
    EFFECTIVE_PROPAGATION_SPEED_MPS,
)


@pytest.fixture(scope="session")
def aik_keypair() -> Tuple[rsa.RSAPrivateKey, bytes]:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_key, public_pem


@pytest.fixture
def golden_pcr_digest() -> bytes:
    return hashlib.sha256(b"CORRIDOR-BARE-METAL-SECURE-BOOT-PCRS-0-7-14").digest()


@pytest.fixture
def attestation_engine(golden_pcr_digest: bytes) -> HardwareAttestationEngine:
    profiles = {
        "CLE-WESTLAKE-01": golden_pcr_digest,
        "CLE-VALLEYVIEW-02": golden_pcr_digest,
    }
    return HardwareAttestationEngine(allowed_pcr_digests=profiles, max_processing_jitter_ms=4.5)


@pytest.fixture
def neo_coordinates() -> Tuple[GeoCoordinates, GeoCoordinates]:
    westlake = GeoCoordinates(latitude=41.4553, longitude=-81.9179, elevation_m=216.0)
    valleyview = GeoCoordinates(latitude=41.3895, longitude=-81.6054, elevation_m=185.0)
    return westlake, valleyview


def test_speed_of_light_rtt_nominal(attestation_engine: HardwareAttestationEngine, neo_coordinates: Tuple[GeoCoordinates, GeoCoordinates]):
    westlake, valleyview = neo_coordinates
    challenge = attestation_engine.generate_proximity_challenge("CLE-VALLEYVIEW-02", valleyview)
    dist_m = attestation_engine.calculate_great_circle_distance_m(westlake, valleyview)
    simulated_elapsed_sec = ((2.0 * dist_m) / EFFECTIVE_PROPAGATION_SPEED_MPS) + 0.0012
    recv_timestamp_ns = challenge.timestamp_sent_ns + int(simulated_elapsed_sec * 1e9)

    valid, msg, actual_rtt = attestation_engine.verify_speed_of_light_rtt(challenge, westlake, recv_timestamp_ns)
    assert valid is True
    assert "Physical Grounding Confirmed" in msg


def test_tier0_egress_full_promotion_gate():
    privkey = ed25519.Ed25519PrivateKey.generate()
    pubkey_pem = privkey.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    issuer = AuthorityTokenIssuer(private_key=privkey)
    controller = Tier0PromotionController(authorized_sovereign_pubkey_pem=pubkey_pem)
    token = issuer.generate_tier0_egress_token(validity_window_sec=300)

    neo_quorum = {
        "CLE-WESTLAKE-01": True,
        "CLE-VALLEYVIEW-02": True,
        "CLE-METROHEALTH-03": True,
        "EAST-LAKE-04": True,
        "SOUTH-AKRON-CANTON-05": True,
    }

    result = controller.execute_tier0_egress_transition(
        token=token,
        tpm_corridor_attestation_results=neo_quorum,
        grok_attack_002_passed=True,
        substation_variance_pct=0.12,
        safe_harbor_violations=0
    )

    assert result["status"] == "PROMOTION_SUCCESSFUL"
    assert result["tier0_state"] == "PRODUCTION_ROOT_ANCHOR"
    assert result["egress_enabled"] is True
