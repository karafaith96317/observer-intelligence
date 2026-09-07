#!/usr/bin/env python3

from src.aetheris_root_enrollment import (
    OperationalNode,
    RootAuthority,
    create_node_enrollment,
    verify_node_enrollment,
)


def main() -> None:
    # DEMO ONLY. Replace these seed values with separately protected secret material
    # when integrating into the Aetheris runtime. Never commit production root seeds.
    root = RootAuthority(b"DEMO_ROOT_SEED_CHANGE_ME")
    node = OperationalNode(b"DEMO_NODE_SEED_CHANGE_ME")

    packet = create_node_enrollment(root, node, ttl_seconds=300)
    valid, reason = verify_node_enrollment(packet)

    print("ROOT_DID:", packet["enrollment"]["root_did"])
    print("NODE_DID:", packet["enrollment"]["node_did"])
    print("SCOPES:", ",".join(packet["enrollment"]["scopes"]))
    print("EXTERNAL_DELIVERY_ENABLED:", packet["enrollment"]["external_delivery_enabled"])
    print("VERIFICATION:", valid, reason)

    if not valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
