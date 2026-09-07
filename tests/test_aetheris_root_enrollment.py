import copy

from src.aetheris_root_enrollment import (
    OperationalNode,
    RootAuthority,
    create_node_enrollment,
    verify_node_enrollment,
)


def test_root_enrollment_verifies():
    root = RootAuthority(b"root-test-seed")
    node = OperationalNode(b"node-test-seed")
    packet = create_node_enrollment(root, node, ttl_seconds=300)

    valid, reason = verify_node_enrollment(packet)

    assert valid is True
    assert reason == "ROOT_AUTHORITY_VERIFIED"
    assert packet["enrollment"]["external_delivery_enabled"] is False


def test_tampered_node_key_is_rejected():
    root = RootAuthority(b"root-test-seed")
    node = OperationalNode(b"node-test-seed")
    packet = create_node_enrollment(root, node, ttl_seconds=300)
    tampered = copy.deepcopy(packet)
    tampered["enrollment"]["node_public_key"] = "00" * 32

    valid, reason = verify_node_enrollment(tampered)

    assert valid is False
    assert reason in {"NODE_DID_KEY_MISMATCH", "ENROLLMENT_ID_MISMATCH", "INVALID_ROOT_SIGNATURE"}


def test_tampered_scope_is_rejected():
    root = RootAuthority(b"root-test-seed")
    node = OperationalNode(b"node-test-seed")
    packet = create_node_enrollment(root, node, ttl_seconds=300)
    tampered = copy.deepcopy(packet)
    tampered["enrollment"]["scopes"].append("EXTERNAL_SEND")

    valid, reason = verify_node_enrollment(tampered)

    assert valid is False
    assert reason in {"ENROLLMENT_ID_MISMATCH", "INVALID_ROOT_SIGNATURE"}


def test_external_delivery_cannot_be_enabled_in_initial_enrollment():
    root = RootAuthority(b"root-test-seed")
    node = OperationalNode(b"node-test-seed")
    packet = create_node_enrollment(root, node, ttl_seconds=300)
    tampered = copy.deepcopy(packet)
    tampered["enrollment"]["external_delivery_enabled"] = True

    valid, reason = verify_node_enrollment(tampered)

    assert valid is False
    assert reason == "EXTERNAL_DELIVERY_MUST_BE_DISABLED"


def test_wrong_root_signature_is_rejected():
    root = RootAuthority(b"root-test-seed")
    other_root = RootAuthority(b"other-root-test-seed")
    node = OperationalNode(b"node-test-seed")
    packet = create_node_enrollment(root, node, ttl_seconds=300)

    # Replace only the signature with one produced by another root.
    packet["root_signature"] = other_root.sign(b"not-the-enrollment")

    valid, reason = verify_node_enrollment(packet)

    assert valid is False
    assert reason == "INVALID_ROOT_SIGNATURE"
