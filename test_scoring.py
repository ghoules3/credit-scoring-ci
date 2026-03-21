from scoring_model import score_client


def test_score_client_low_risk():
    assert score_client(limit_bal=120000, pay_delay=0, age=30) == "low"


def test_score_client_medium_risk_due_to_age():
    assert score_client(limit_bal=120000, pay_delay=0, age=22) == "medium"


def test_score_client_high_risk_due_to_low_limit():
    assert score_client(limit_bal=30000, pay_delay=0, age=35) == "high"


def test_score_client_high_risk_due_to_delay():
    assert score_client(limit_bal=120000, pay_delay=3, age=35) == "high"