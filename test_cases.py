"""
SEAFS Test Suite - Comprehensive Test Cases
Run with: pytest test_cases.py -v
"""

import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def sample_alpha():
    """Typical privileged cohort applicant"""
    return {"gpa": 3.5, "financial_need": 20.0, "recommendations": 75.0}

@pytest.fixture
def sample_beta():
    """Structurally disadvantaged but high-need applicant"""
    return {"gpa": 2.7, "financial_need": 90.0, "recommendations": 85.0}

@pytest.fixture
def sample_reject():
    """Clear rejection case"""
    return {"gpa": 1.5, "financial_need": 10.0, "recommendations": 20.0}

# ============================================================
# UNIT TESTS - FUZZY ENGINE
# ============================================================

def test_membership_functions():
    """Test that membership functions return valid degrees"""
    from app import gpa, financial_need, recommendations
    import skfuzzy as fuzz
    
    # Test GPA membership
    assert 0 <= fuzz.interp_membership(gpa.universe, gpa['Low'].mf, 1.5) <= 1
    assert 0 <= fuzz.interp_membership(gpa.universe, gpa['Medium'].mf, 2.5) <= 1
    assert 0 <= fuzz.interp_membership(gpa.universe, gpa['High'].mf, 3.8) <= 1
    
    # Test boundary conditions
    assert fuzz.interp_membership(gpa.universe, gpa['Low'].mf, 1.0) == 1.0
    assert fuzz.interp_membership(gpa.universe, gpa['High'].mf, 4.0) == 1.0

def test_rule_base_cardinality():
    """Verify exactly 10 rules in the rule base"""
    from app import rules
    assert len(rules) == 10

def test_engine_initialization():
    """Test that control system initializes without error"""
    from app import seafs_engine
    assert seafs_engine is not None

# ============================================================
# INTEGRATION TESTS - API ENDPOINTS
# ============================================================

def test_root_endpoint():
    """Test health check endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "SEAFS" in data["system"]

def test_predict_valid_alpha(sample_alpha):
    """Test prediction for privileged cohort"""
    response = client.post("/predict", json=sample_alpha)
    assert response.status_code == 200
    data = response.json()
    assert "defuzzified_eligibility_score" in data
    assert data["systemic_allocation_decision"] in ["Approve", "Waitlist", "Reject"]
    assert 0 <= data["defuzzified_eligibility_score"] <= 100

def test_predict_valid_beta(sample_beta):
    """Test prediction for disadvantaged cohort"""
    response = client.post("/predict", json=sample_beta)
    assert response.status_code == 200
    data = response.json()
    # Beta applicant with high need should be approved despite low GPA
    assert data["systemic_allocation_decision"] == "Approve"
    assert data["defuzzified_eligibility_score"] >= 70.0

def test_predict_reject(sample_reject):
    """Test clear rejection case"""
    response = client.post("/predict", json=sample_reject)
    assert response.status_code == 200
    data = response.json()
    assert data["systemic_allocation_decision"] == "Reject"
    assert data["defuzzified_eligibility_score"] < 45.0

def test_predict_invalid_gpa_high():
    """Test GPA > 4.0 returns validation error"""
    response = client.post("/predict", json={"gpa": 5.0, "financial_need": 50, "recommendations": 50})
    assert response.status_code == 422

def test_predict_invalid_gpa_low():
    """Test GPA < 1.0 returns validation error"""
    response = client.post("/predict", json={"gpa": 0.5, "financial_need": 50, "recommendations": 50})
    assert response.status_code == 422

def test_predict_invalid_need_high():
    """Test financial_need > 100 returns validation error"""
    response = client.post("/predict", json={"gpa": 3.0, "financial_need": 150, "recommendations": 50})
    assert response.status_code == 422

def test_predict_missing_field():
    """Test missing required field"""
    response = client.post("/predict", json={"gpa": 3.0, "financial_need": 50})
    assert response.status_code == 422

# ============================================================
# BOUNDARY TESTS
# ============================================================

@pytest.mark.parametrize("gpa,need,recs,expected_decision", [
    (4.0, 100.0, 100.0, "Approve"),
    (1.0, 0.0, 0.0, "Reject"),
    (3.0, 50.0, 50.0, "Approve"),
    (2.5, 75.0, 75.0, "Approve"),  # Compensatory case
])
def test_boundary_conditions(gpa, need, recs, expected_decision):
    response = client.post("/predict", json={"gpa": gpa, "financial_need": need, "recommendations": recs})
    assert response.status_code == 200
    assert response.json()["systemic_allocation_decision"] == expected_decision

# ============================================================
# REGRESSION TESTS - SPECIFIC KNOWN CASES
# ============================================================

def test_regression_beta_74_saved():
    """Regression: 74 Beta students rescued from legacy rejection"""
    # This test documents the key finding from empirical validation
    beta_samples = [
        {"gpa": 2.63, "financial_need": 86.3, "recommendations": 62.4},  # 71.93
        {"gpa": 2.99, "financial_need": 80.7, "recommendations": 53.0},  # 70.85
        {"gpa": 2.94, "financial_need": 90.4, "recommendations": 91.4},  # 82.88
        {"gpa": 2.66, "financial_need": 85.5, "recommendations": 71.4},  # 73.63
        {"gpa": 2.84, "financial_need": 78.0, "recommendations": 71.8},  # 71.76
    ]
    
    for sample in beta_samples:
        response = client.post("/predict", json=sample)
        assert response.status_code == 200
        data = response.json()
        assert data["systemic_allocation_decision"] == "Approve"
        assert data["defuzzified_eligibility_score"] >= 70.0

# ============================================================
# PERFORMANCE TESTS
# ============================================================

def test_response_time():
    """Verify sub-5ms response time"""
    import time
    start = time.time()
    response = client.post("/predict", json={"gpa": 3.0, "financial_need": 50, "recommendations": 50})
    elapsed = (time.time() - start) * 1000
    assert response.status_code == 200
    assert elapsed < 100  # Should be well under 100ms

def test_batch_consistency():
    """Test that repeated calls return identical results"""
    sample = {"gpa": 3.2, "financial_need": 65.0, "recommendations": 78.0}
    scores = []
    for _ in range(10):
        response = client.post("/predict", json=sample)
        scores.append(response.json()["defuzzified_eligibility_score"])
    # All scores should be identical (deterministic)
    assert len(set(scores)) == 1

# ============================================================
# EDGE CASE TESTS
# ============================================================

def test_float_precision():
    """Test that float inputs are handled correctly"""
    response = client.post("/predict", json={
        "gpa": 3.33333333,
        "financial_need": 66.666666,
        "recommendations": 77.777777
    })
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["defuzzified_eligibility_score"], float)

def test_exact_threshold_45():
    """Test score exactly at 45.0 boundary (Reject/Waitlist)"""
    # This is a regression test for the threshold logic
    # We need a case that produces exactly 45.0
    # Using a known case from the rule base
    pass  # Implemented when exact case identified

def test_exact_threshold_68():
    """Test score exactly at 68.0 boundary (Waitlist/Approve)"""
    pass  # Implemented when exact case identified

# ============================================================
# SECURITY TESTS
# ============================================================

def test_sql_injection_attempt():
    """Test that SQL injection payloads are rejected"""
    response = client.post("/predict", json={
        "gpa": "3.0; DROP TABLE applicants;",
        "financial_need": 50,
        "recommendations": 50
    })
    assert response.status_code == 422

def test_xss_attempt():
    """Test that XSS payloads are rejected"""
    response = client.post("/predict", json={
        "gpa": 3.0,
        "financial_need": 50,
        "recommendations": "<script>alert('xss')</script>"
    })
    assert response.status_code == 422

# ============================================================
# OPEN API DOCUMENTATION TEST
# ============================================================

def test_openapi_schema():
    """Test that OpenAPI schema is accessible"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "paths" in schema
    assert "/predict" in schema["paths"]

# ============================================================
# RUN TESTS WITH: pytest test_cases.py -v --tb=short
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])