"""Schema validation tests for the locked OI v0.1 JSON Schema contracts.

These fixtures validate the repository's actual Draft 2020-12 schemas directly.
They are intentionally separate from runtime dataclass/unit tests because the
JSON contracts and Python runtime currently use partially different field names.
"""

import json
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).parent.parent
SCHEMAS_DIR = REPO_ROOT / "schemas"


def validator(name):
    schema = json.loads((SCHEMAS_DIR / name).read_text())
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


VALID = {
    "authority-token.schema.json": {
        "token_id": "TOK-001",
        "scope": "execute-action:migrate",
        "not_before": "2026-08-31T14:00:00Z",
        "not_after": "2026-08-31T14:05:00Z",
        "evidence_refs": ["OBS-001"],
        "issuer": "authorizer:root",
        "issued_at": "2026-08-31T14:00:00Z",
        "binding": {"method": "ed25519", "value": "fixture-signature"},
    },
    "shadow-evaluation.schema.json": {
        "evaluation_id": "SHAD-001",
        "critic_id": "critic-01",
        "created_at": "2026-08-31T14:01:00Z",
        "input_scope": {
            "observation_refs": ["OBS-001"],
            "information_received_summary": "Raw observation only",
            "received_interpretations": False,
        },
        "isolation_flag": True,
        "correlation_with_primary": {
            "shared_upstream_data": False,
            "estimated_dependence": 0.05,
        },
        "findings": {
            "contradictions": [],
            "alternative_hypotheses": ["alternate"],
            "semantic_leap_flags": [],
        },
        "uncertainty": 0.1,
    },
    "reconciliation.schema.json": {
        "reconciliation_id": "REC-001",
        "created_at": "2026-08-31T14:02:00Z",
        "contributing_observations": [
            {"observation_id": "OBS-001", "resolvable": True, "weight_or_credit": 1.0}
        ],
        "shadow_evaluation_refs": ["SHAD-001"],
        "dependence_summary": {
            "method": "graded-rho",
            "effective_independent_pathways": 1.0,
            "pairwise_notes": [],
        },
        "retained_disagreement": [],
        "disclosure_boundaries": [],
        "lineage": {
            "transformation_summary": "Direct grounded reconciliation",
            "excluded_or_downweighted": [],
        },
        "completeness": {
            "all_refs_resolvable": True,
            "missing_fields": [],
            "score": 1.0,
        },
    },
    "action-authorization.schema.json": {
        "authorization_id": "AUTH-001",
        "created_at": "2026-08-31T14:03:00Z",
        "decision": "authorize",
        "authority_token_ref": "TOK-001",
        "reconciliation_ref": "REC-001",
        "token_revalidation": {
            "binding_verified": True,
            "scope_match": True,
            "time_window_valid": True,
            "evidence_refs_still_resolvable": True,
            "checked_at": "2026-08-31T14:03:00Z",
            "failure_reasons": [],
        },
        "escalation_flag": False,
        "process_metrics": {
            "independence_estimation_error": 0.0,
            "provenance_reconstruction_accuracy": 1.0,
            "contradiction_preservation": True,
        },
    },
}


@pytest.mark.parametrize("schema_name", sorted(VALID))
def test_positive_fixtures(schema_name):
    errors = list(validator(schema_name).iter_errors(VALID[schema_name]))
    assert not errors, [e.message for e in errors]


NEGATIVE_MUTATIONS = [
    ("authority-token.schema.json", lambda x: x.pop("binding")),
    ("authority-token.schema.json", lambda x: x.__setitem__("evidence_refs", [])),
    ("shadow-evaluation.schema.json", lambda x: x.pop("input_scope")),
    ("shadow-evaluation.schema.json", lambda x: x.__setitem__("uncertainty", 1.5)),
    ("reconciliation.schema.json", lambda x: x["completeness"].__setitem__("score", -0.1)),
    ("reconciliation.schema.json", lambda x: x.pop("lineage")),
    ("action-authorization.schema.json", lambda x: x.pop("token_revalidation")),
    ("action-authorization.schema.json", lambda x: x["token_revalidation"].pop("scope_match")),
    ("action-authorization.schema.json", lambda x: x.__setitem__("decision", "self_attested_execute")),
]


@pytest.mark.parametrize("schema_name,mutate", NEGATIVE_MUTATIONS)
def test_negative_fixtures(schema_name, mutate):
    fixture = deepcopy(VALID[schema_name])
    mutate(fixture)
    errors = list(validator(schema_name).iter_errors(fixture))
    assert errors, f"Expected {schema_name} malformed fixture to fail"
