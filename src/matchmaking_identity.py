"""Identity boundary for LucidFluence / ERA-GOS matchmaking.

Tier 0 is reserved for internal/self-loop validation. Tier 1 is reserved for
compatible candidates whose identity is distinct from the local system.
"""
from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet


class MatchTier(Enum):
    TIER_0_SELF_CHECK = "TIER_0_SELF_CHECK"
    TIER_1_EXTERNAL_MATCH = "TIER_1_EXTERNAL_MATCH"
    NOT_ELIGIBLE = "NOT_ELIGIBLE"


@dataclass(frozen=True)
class MatchCandidate:
    node_id: str
    system_id: str
    protocol_version: str
    capabilities: FrozenSet[str]


@dataclass(frozen=True)
class MatchDecision:
    tier: MatchTier
    compatibility_score: float
    reason: str


def classify_candidate(
    local_system_id: str,
    required_protocol_version: str,
    required_capabilities: FrozenSet[str],
    candidate: MatchCandidate,
) -> MatchDecision:
    """Classify a candidate without allowing self-identity into Tier 1.

    Compatibility is the fraction of required capabilities supplied by the
    candidate, with exact protocol-version compatibility required for Tier 1.
    A candidate carrying the local system identity is always Tier 0 regardless
    of its compatibility score.
    """
    if required_capabilities:
        overlap = len(required_capabilities.intersection(candidate.capabilities))
        score = overlap / len(required_capabilities)
    else:
        score = 1.0

    if candidate.system_id == local_system_id:
        return MatchDecision(
            MatchTier.TIER_0_SELF_CHECK,
            score,
            "Candidate shares local system identity; retain for internal loopback validation only.",
        )

    if candidate.protocol_version != required_protocol_version:
        return MatchDecision(
            MatchTier.NOT_ELIGIBLE,
            score,
            "External identity confirmed, but protocol version is incompatible.",
        )

    if score < 1.0:
        return MatchDecision(
            MatchTier.NOT_ELIGIBLE,
            score,
            "External identity confirmed, but required capabilities are incomplete.",
        )

    return MatchDecision(
        MatchTier.TIER_1_EXTERNAL_MATCH,
        score,
        "Distinct external identity with exact protocol and capability compatibility.",
    )
