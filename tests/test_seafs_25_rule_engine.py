import pytest
from seafs_25_rule_engine import predict_one, MATRIX, OUTPUT_MF_PARAMETERS

def test_rule_matrix_has_27_unique_combinations():
    rows = MATRIX["rules"]
    combos = {(r["gpa"], r["financial_need"], r["recommendations"]) for r in rows}
    assert len(rows) == 27
    assert len(combos) == 27

def test_two_reconstructed_rules_are_explicit():
    inferred = {(r["gpa"], r["financial_need"], r["recommendations"]): r["consequent"]
                for r in MATRIX["rules"] if r["provenance"] == "reconstructed"}
    assert inferred == {
        ("Low", "Low", "Medium"): "Reject",
        ("Low", "Medium", "Medium"): "Waitlist",
    }

@pytest.mark.parametrize("x", [0, 20, 30, 45, 56.5, 68, 78, 100])
def test_output_membership_functions_are_bounded(x):
    import numpy as np
    from seafs_25_rule_engine import _mf
    for kind, params in OUTPUT_MF_PARAMETERS.values():
        y = _mf(np.array([float(x)]), kind, params)
        assert 0.0 <= float(y[0]) <= 1.0

@pytest.mark.parametrize("case", [(0,0,0),(50,50,50),(100,100,100),(40,80,90),(60,20,40)])
def test_engine_returns_auditable_result(case):
    result = predict_one(*case)
    assert result["decision_band"] in {"Reject","Waitlist","Approve","NoRuleFired"}
    assert result["model_metadata"]["rule_count"] == 27
    if result["decision_band"] != "NoRuleFired":
        assert 0 <= result["score"] <= 100
        assert result["rule_trace"]

def test_boundary_bands_are_explicit():
    from seafs_25_rule_engine import _decision
    assert _decision(44.999) == "Reject"
    assert _decision(45.0) == "Waitlist"
    assert _decision(67.999) == "Waitlist"
    assert _decision(68.0) == "Approve"

@pytest.mark.parametrize("case", [(-1,50,50),(50,101,50),(50,50,float("nan"))])
def test_invalid_inputs_raise(case):
    with pytest.raises(ValueError):
        predict_one(*case)

def test_borderline_rule_is_human_review_flag():
    # Input values are chosen to activate a rule whose appendix consequent is Borderline.
    result = predict_one(20, 20, 80)
    assert result["human_review_required"] is True
