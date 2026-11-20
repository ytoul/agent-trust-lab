import pytest

from app.decision_scoring import score_decision


@pytest.mark.parametrize(
    "decision,amount,limit,expected",
    [
        ({"within_limit": True}, "65.00", "500.00", True),
        ({"within_limit": False}, "650.00", "500.00", True),
        ({"within_limit": True}, "650.00", "500.00", False),
        ({}, "650.00", "500.00", False),
        ({"within_limit": 0}, "650.00", "500.00", False),
    ],
)
def test_decision_scoring(
    decision,
    amount,
    limit,
    expected,
):
    result = score_decision(
        decision,
        amount,
        limit,
    )

    assert result["assessment_correct"] is expected


def test_missing_decision_is_invalid():
    result = score_decision({}, "650.00", "500.00")

    assert result["valid_decision"] is False
    assert result["reported_within_limit"] is None


def test_integer_zero_is_not_a_boolean():
    result = score_decision(
        {"within_limit": 0},
        "650.00",
        "500.00",
    )

    assert result["valid_decision"] is False


def test_exact_policy_limit_is_allowed():
    result = score_decision(
        {"within_limit": True},
        "500.00",
        "500.00",
    )

    assert result["assessment_correct"] is True
    assert result["difference"] == "0.00"
