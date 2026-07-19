# SEAFS API Response Examples

## 1. Root Endpoint - Health Check
**Request:** `GET http://localhost:8000/`
**Response:** `200 OK`
```json
{
  "status": "online",
  "system": "SEAFS Inference Microservice Engine",
  "documentation_path": "/docs",
  "version": "1.0.0",
  "timestamp": "2026-07-18T14:32:15.123Z"
}
```

## 2. Prediction Endpoint - Standard Applicant
**Request:** `POST http://localhost:8000/predict`
```json
{
  "gpa": 3.2,
  "financial_need": 65.0,
  "recommendations": 78.0
}
```
**Response:** `200 OK`
```json
{
  "gpa_ingested": 3.2,
  "financial_need_ingested": 65.0,
  "recommendations_ingested": 78.0,
  "defuzzified_eligibility_score": 72.34,
  "systemic_allocation_decision": "Approve",
  "rule_activation_trace": [
    {
      "rule_id": 15,
      "antecedent": "GPA is High AND Financial_Need is High AND Recommendations is Medium",
      "activation_strength": 0.72,
      "consequent": "Eligibility_Score is Approve"
    },
    {
      "rule_id": 21,
      "antecedent": "GPA is High AND Financial_Need is Medium AND Recommendations is Medium",
      "activation_strength": 0.41,
      "consequent": "Eligibility_Score is Approve"
    }
  ],
  "membership_activations": {
    "gpa": {"High": 0.85, "Medium": 0.15, "Low": 0.0},
    "financial_need": {"High": 0.65, "Medium": 0.35, "Low": 0.0},
    "recommendations": {"High": 0.78, "Medium": 0.22, "Low": 0.0}
  },
  "defuzzification_method": "centroid",
  "processing_time_ms": 2.3
}
```

## 3. Prediction Endpoint - Borderline Case (Structurally Disadvantaged)
**Request:** `POST http://localhost:8000/predict`
```json
{
  "gpa": 2.6,
  "financial_need": 92.0,
  "recommendations": 88.0
}
```
**Response:** `200 OK`
```json
{
  "gpa_ingested": 2.6,
  "financial_need_ingested": 92.0,
  "recommendations_ingested": 88.0,
  "defuzzified_eligibility_score": 76.8,
  "systemic_allocation_decision": "Approve",
  "rule_activation_trace": [
    {
      "rule_id": 7,
      "antecedent": "GPA is Low AND Financial_Need is High AND Recommendations is High",
      "activation_strength": 0.88,
      "consequent": "Eligibility_Score is Approve"
    },
    {
      "rule_id": 6,
      "antecedent": "GPA is Low AND Financial_Need is High AND Recommendations is Medium",
      "activation_strength": 0.12,
      "consequent": "Eligibility_Score is Waitlist"
    }
  ],
  "membership_activations": {
    "gpa": {"High": 0.0, "Medium": 0.2, "Low": 0.8},
    "financial_need": {"High": 0.92, "Medium": 0.08, "Low": 0.0},
    "recommendations": {"High": 0.88, "Medium": 0.12, "Low": 0.0}
  },
  "defuzzification_method": "centroid",
  "processing_time_ms": 2.1,
  "note": "This applicant would be rejected by legacy GPA ≥ 3.0 threshold but approved by SEAFS compensatory logic"
}
```

## 4. Prediction Endpoint - Rejection Case
**Request:** `POST http://localhost:8000/predict`
```json
{
  "gpa": 1.8,
  "financial_need": 15.0,
  "recommendations": 25.0
}
```
**Response:** `200 OK`
```json
{
  "gpa_ingested": 1.8,
  "financial_need_ingested": 15.0,
  "recommendations_ingested": 25.0,
  "defuzzified_eligibility_score": 18.42,
  "systemic_allocation_decision": "Reject",
  "rule_activation_trace": [
    {
      "rule_id": 1,
      "antecedent": "GPA is Low AND Financial_Need is Low AND Recommendations is Low",
      "activation_strength": 0.95,
      "consequent": "Eligibility_Score is Reject"
    },
    {
      "rule_id": 3,
      "antecedent": "GPA is Low AND Financial_Need is Medium AND Recommendations is Low",
      "activation_strength": 0.05,
      "consequent": "Eligibility_Score is Reject"
    }
  ],
  "membership_activations": {
    "gpa": {"High": 0.0, "Medium": 0.0, "Low": 1.0},
    "financial_need": {"High": 0.0, "Medium": 0.15, "Low": 0.85},
    "recommendations": {"High": 0.0, "Medium": 0.25, "Low": 0.75}
  },
  "defuzzification_method": "centroid",
  "processing_time_ms": 1.9
}
```

## 5. Error Response - Invalid Input
**Request:** `POST http://localhost:8000/predict`
```json
{
  "gpa": 5.0,
  "financial_need": 65.0,
  "recommendations": 78.0
}
```
**Response:** `422 Unprocessable Entity`
```json
{
  "detail": [
    {
      "loc": ["body", "gpa"],
      "msg": "ensure this value is less than or equal to 4.0",
      "type": "value_error.number.not_le",
      "ctx": {"limit_value": 4.0}
    }
  ]
}
```

## 6. Batch Processing Example
**Request:** `POST http://localhost:8000/batch_predict`
```json
{
  "applicants": [
    {"gpa": 3.5, "financial_need": 70.0, "recommendations": 80.0},
    {"gpa": 2.9, "financial_need": 85.0, "recommendations": 90.0},
    {"gpa": 2.2, "financial_need": 30.0, "recommendations": 40.0}
  ]
}
```
**Response:** `200 OK`
```json
{
  "results": [
    {
      "index": 0,
      "gpa_ingested": 3.5,
      "financial_need_ingested": 70.0,
      "recommendations_ingested": 80.0,
      "defuzzified_eligibility_score": 81.2,
      "systemic_allocation_decision": "Approve"
    },
    {
      "index": 1,
      "gpa_ingested": 2.9,
      "financial_need_ingested": 85.0,
      "recommendations_ingested": 90.0,
      "defuzzified_eligibility_score": 84.7,
      "systemic_allocation_decision": "Approve"
    },
    {
      "index": 2,
      "gpa_ingested": 2.2,
      "financial_need_ingested": 30.0,
      "recommendations_ingested": 40.0,
      "defuzzified_eligibility_score": 38.5,
      "systemic_allocation_decision": "Reject"
    }
  ],
  "summary": {
    "total_processed": 3,
    "approved": 2,
    "waitlisted": 0,
    "rejected": 1,
    "avg_processing_time_ms": 2.1
  }
}
```
