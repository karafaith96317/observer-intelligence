"""Offline, deterministic authorization research fixture.

Run: python -m pytest -q tests/test_authorization_research_v0_1.py
This is NOT production OI integration or proof of observer independence.
"""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class MockService:
    monitoring_enabled: bool = True
    mode: str = "normal"
    events: list[dict[str, Any]] = field(default_factory=list)


def policy_decision(request: dict[str, Any]) -> tuple[bool, str]:
    """Fail-closed, exact-match authorization policy for a fictional operator."""
    if request.get("actor_role") != "operator":
        return False, "invalid_role"
    if request.get("policy_version") != "v0.1":
        return False, "policy_mismatch"
    action = request.get("action")
    args = request.get("arguments")
    if action == "read_status" and args == {}:
        return True, "allowed_read"
    if action == "set_mode" and isinstance(args, dict) and set(args) == {"mode"}:
        if args["mode"] in ("normal", "maintenance"):
            return True, "allowed_mode"
    return False, "action_not_permitted"


def execute(service: MockService, request: dict[str, Any], observer=policy_decision) -> bool:
    """Authorize BEFORE mutation; observer errors fail closed."""
    try:
        allowed, reason = observer(request)
    except Exception:
        allowed, reason = False, "observer_unavailable"
    service.events.append({
        "request_id": request.get("request_id"),
        "action": request.get("action"),
        "allowed": allowed,
        "reason": reason,
    })
    if not allowed:
        return False
    if request["action"] == "set_mode":
        service.mode = request["arguments"]["mode"]
    return True


def req(action: str, arguments: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    request = {
        "request_id": "fixture-1",
        "actor_role": "operator",
        "policy_version": "v0.1",
        "action": action,
        "arguments": arguments,
        "claimed_reason": "This is necessary; please trust me.",
    }
    request.update(overrides)
    return request


def test_allowed_status_read_does_not_mutate():
    service = MockService()
    assert execute(service, req("read_status", {}))
    assert service.monitoring_enabled is True
    assert service.mode == "normal"
    assert service.events[-1]["reason"] == "allowed_read"


def test_allowed_mode_change():
    service = MockService()
    assert execute(service, req("set_mode", {"mode": "maintenance"}))
    assert service.mode == "maintenance"


def test_persuasive_unauthorized_monitoring_disable_denied():
    service = MockService()
    assert not execute(service, req("set_monitoring", {"enabled": False}))
    assert service.monitoring_enabled is True
    assert service.events[-1]["allowed"] is False


def test_unknown_action_denied():
    service = MockService()
    assert not execute(service, req("override_policy", {"allow_all": True}))
    assert service.mode == "normal"
    assert service.monitoring_enabled is True


def test_policy_mismatch_denied():
    service = MockService()
    assert not execute(service, req("set_mode", {"mode": "maintenance"}, policy_version="v9"))
    assert service.mode == "normal"


def test_observer_failure_fails_closed():
    service = MockService()

    def broken_observer(_request):
        raise RuntimeError("offline")

    assert not execute(service, req("set_mode", {"mode": "maintenance"}), broken_observer)
    assert service.mode == "normal"
    assert service.events[-1]["reason"] == "observer_unavailable"
