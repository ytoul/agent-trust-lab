import json

import app.read_only_agent as agent


def test_payment_tool_blocked(monkeypatch):
    """
    A read-only agent must never execute payment tools.
    """

    def forbidden_dispatch(*args, **kwargs):
        raise AssertionError(
            "Payment tool reached the dispatcher!"
        )

    monkeypatch.setattr(
        agent,
        "dispatch_tool",
        forbidden_dispatch,
    )

    result = agent.execute_read_only_tool(
        "simulate_payment",
        json.dumps({"expense_id": 2}),
    )

    assert result["status"] == "blocked"
    assert result["reason"] == (
        "Tool not permitted for read-only agent"
    )
