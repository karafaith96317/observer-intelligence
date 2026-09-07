# Aetheris Root Authority Enrollment

Status: design boundary for integration with the Aetheris/ERA-GOS runtime.

## Purpose

Establish a human-controlled root authorization layer above the Aetheris operational node without conflating human identity, node identity, recipient identity, delivery, or validator acknowledgement.

## Trust roles

- **Root authority**: offline or separately protected Ed25519 key that authorizes operational node enrollment and revocation.
- **Operational node**: separate Ed25519 key used by the Aetheris runtime for scoped actions.
- **Target**: explicitly enrolled recipient identity. A target DID is not trusted unless its public key binding was verified out-of-band.
- **Validator**: independent verifier identity. Validation is separate from delivery and authorization.

## Required evidence boundaries

The runtime MUST preserve these states independently:

1. root key generated
2. node key generated
3. node enrollment signed by root
4. node enrollment independently verified
5. target enrolled and verified
6. action authorization signed
7. delivery attempted
8. delivery confirmed
9. validator acknowledgement verified

A later state MUST NOT be inferred from an earlier state. In particular, signing is not delivery, delivery is not acknowledgement, and a DID string alone is not proof of a real-world identity.

## Migration rule

Existing Aetheris Blocks 0–14 remain immutable legacy history. Their historical identity tags MUST NOT be relabeled as Ed25519 signatures. The first block using the new identity scheme should declare the migration explicitly, e.g. `IDENTITY_SCHEME=ED25519_V1`.

## Fail-closed policy

External delivery remains disabled unless all required target-binding checks pass. Unknown target, public-key mismatch, invalid signature, expired authorization, reused nonce, or missing enrollment results in no external action.

## Recommended initial scope

The first root enrollment should authorize only local ledger and dry-run authorization functions. External send should remain disabled until a verified recipient registry and authenticated transport are implemented and tested.
