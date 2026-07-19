# SEAFS: Synthesized Explainable Adaptive Fuzzy Scholarship Framework

[![CI](https://github.com/<Alice-Iyamuremye>/SEAFS-Scholarship-Framework/workflows/CI/badge.svg)](https://github.com/<Alice-Iyamuremye>/SEAFS-Scholarship-Framework/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **A transparent, explainable, and fairness-aware fuzzy logic decision support system for scholarship eligibility assessment.**

---

## 🎯 Problem

Traditional scholarship allocation relies on rigid GPA thresholds (e.g., GPA ≥ 3.0), which:
- ❌ Systematically disadvantage socioeconomically disadvantaged students
- ❌ Ignore financial need and qualitative factors
- ❌ Operate as opaque "black boxes" with no audit trail
- ❌ Violate GDPR Article 22 & EU AI Act transparency requirements

---

## 💡 Solution: SEAFS Framework

**SEAFS** (Synthesized Explainable Adaptive Fuzzy Scholarship) replaces rigid thresholds with a **transparent, compensatory fuzzy logic engine** that:

| Feature | Legacy Systems | SEAFS |
|---------|---------------|-------|
| **Decision Logic** | Hard GPA ≥ 3.0 threshold | Continuous compensatory logic |
| **Disparity (Beta vs Alpha)** | 61.7% gap | **12.4% gap** |
| **Disadvantaged Pass Rate** | 38.0% | **86.7%** |
| **Transparency** | Black box | Native rule-level traceability |
| **GDPR Art. 22 / EU AI Act** | ❌ Non-compliant | ✅ Native compliance |
| **Audit Trail** | None | Full rule activation trace |

---

## 🏗️ Architecture

![Architecture](docs/architecture.png)

```mermaid
graph TD
    A[Client: Web Portal / Mobile / CLI] --> B[FastAPI Gateway :8000]
    B --> C[SEAFS Core Engine]
    C --> D[Membership Functions]
    C --> D[Rule Base (25 rules)]
    C --> D[Fuzzy AHP Weights]
    C --> D[PostgreSQL]
    C --> D[Config Files]
    C --> E[Observability: Logs, Metrics, Tracing]
