from src.matchmaking_identity import (
    MatchCandidate,
    MatchTier,
    classify_candidate,
)


def test_self_candidate_is_tier_0_even_when_perfectly_compatible():
    candidate = MatchCandidate(
        node_id="LOCAL-NODE-01",
        system_id="LUCIDFLUENCE-LOCAL",
        protocol_version="oi-v0.2.1",
        capabilities=frozenset({"schema-v1", "mtls", "provenance"}),
    )
    decision = classify_candidate(
        local_system_id="LUCIDFLUENCE-LOCAL",
        required_protocol_version="oi-v0.2.1",
        required_capabilities=frozenset({"schema-v1", "mtls", "provenance"}),
        candidate=candidate,
    )
    assert decision.compatibility_score == 1.0
    assert decision.tier is MatchTier.TIER_0_SELF_CHECK


def test_distinct_fully_compatible_candidate_can_reach_tier_1():
    candidate = MatchCandidate(
        node_id="EXT-NODE-77",
        system_id="EXTERNAL-SYSTEM-77",
        protocol_version="oi-v0.2.1",
        capabilities=frozenset({"schema-v1", "mtls", "provenance"}),
    )
    decision = classify_candidate(
        local_system_id="LUCIDFLUENCE-LOCAL",
        required_protocol_version="oi-v0.2.1",
        required_capabilities=frozenset({"schema-v1", "mtls", "provenance"}),
        candidate=candidate,
    )
    assert decision.compatibility_score == 1.0
    assert decision.tier is MatchTier.TIER_1_EXTERNAL_MATCH


def test_external_candidate_with_missing_capability_is_not_tier_1():
    candidate = MatchCandidate(
        node_id="EXT-NODE-88",
        system_id="EXTERNAL-SYSTEM-88",
        protocol_version="oi-v0.2.1",
        capabilities=frozenset({"schema-v1", "mtls"}),
    )
    decision = classify_candidate(
        local_system_id="LUCIDFLUENCE-LOCAL",
        required_protocol_version="oi-v0.2.1",
        required_capabilities=frozenset({"schema-v1", "mtls", "provenance"}),
        candidate=candidate,
    )
    assert decision.compatibility_score == 2 / 3
    assert decision.tier is MatchTier.NOT_ELIGIBLE


def test_external_candidate_with_protocol_mismatch_is_not_tier_1():
    candidate = MatchCandidate(
        node_id="EXT-NODE-99",
        system_id="EXTERNAL-SYSTEM-99",
        protocol_version="oi-v0.2.0",
        capabilities=frozenset({"schema-v1", "mtls", "provenance"}),
    )
    decision = classify_candidate(
        local_system_id="LUCIDFLUENCE-LOCAL",
        required_protocol_version="oi-v0.2.1",
        required_capabilities=frozenset({"schema-v1", "mtls", "provenance"}),
        candidate=candidate,
    )
    assert decision.compatibility_score == 1.0
    assert decision.tier is MatchTier.NOT_ELIGIBLE
