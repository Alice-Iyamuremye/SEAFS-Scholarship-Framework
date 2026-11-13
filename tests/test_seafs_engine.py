import numpy as np
import pandas as pd
import pytest
from seafs_engine import SEAFSEngine

def test_complete_rule_base():
    assert len(SEAFSEngine().rule_base) == 27

@pytest.mark.parametrize("values", [
    (0, 0, 0), (100, 100, 100), (50, 50, 50),
    (40, 80, 90), (60, 20, 40), (99.9, 0.1, 50)
])
def test_valid_inputs_produce_finite_outputs(values):
    result = SEAFSEngine().predict_one(*values)
    assert np.isfinite(result.score)
    assert 0 <= result.score <= 100
    assert result.decision in {"Reject", "Waitlist", "Approve"}
    assert len(result.rule_trace) > 0

@pytest.mark.parametrize("values", [
    (-1, 50, 50), (50, 101, 50), (50, 50, float("nan"))
])
def test_invalid_inputs_raise(values):
    with pytest.raises(ValueError):
        SEAFSEngine().predict_one(*values)

def test_weights_are_normalized():
    engine = SEAFSEngine({"gpa": 3, "financial_need": 5, "recommendations": 2})
    assert sum(engine.weights.values()) == pytest.approx(1.0)
    assert engine.weights["financial_need"] == pytest.approx(0.5)

def test_batch_prediction():
    frame = pd.DataFrame({
        "gpa_0_100": [20, 50, 90],
        "financial_need": [90, 50, 10],
        "recommendations": [90, 50, 90],
    })
    result = SEAFSEngine().predict(frame)
    assert len(result) == 3
    assert result["seafs_score"].between(0, 100).all()
