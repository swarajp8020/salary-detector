# Salary Intelligence Engine (Phase 1 – MVP)

## 🎯 Objective

Build a backend service that identifies whether a customer account behaves like a **salary account**, classifies user behavior, and detects churn risk based on transaction patterns.

## ✅ What We Built

### 1. Salary Detection Engine

* Identifies salary accounts using transaction history
* Works for:

  * Monthly salary
  * Weekly wages
  * Multi-month patterns

### 2. Feature Engineering Layer

We extract behavioral signals from transactions:

* `interval_mean` → salary frequency (monthly/weekly)
* `interval_std` → consistency of salary dates
* `amount_mean` → average credited amount
* `amount_std` → stability of salary amount
* `count` → number of occurrences

### 3. Scoring Algorithm (Heuristic Model)

We compute a confidence score using weighted signals:

```python
score =
    0.6 * time_score +
    0.25 * amount_score +
    0.15 * count_score +
    salary_boost
```

* Higher score ⇒ higher likelihood of salary account
* Threshold-based classification (MVP)

---

### 4. Scenario Classification Engine

We classify customers into 3 behavioral segments:

| Scenario | Meaning                | Business Insight |
| -------- | ---------------------- | ---------------- |
| A        | Normal usage           | Active user      |
| B        | Salary drained quickly | Retention risk   |
| C        | Salary stopped         | Churn risk       |

### 5. Churn Detection Logic

* Detects if expected salary is missing
* Uses pattern-based inference (interval + history)
* Handles:

  * Monthly salary
  * Weekly salary
  * Limited historical data

### 6. Explainable Output (Bank-Grade Requirement)

Example response:

```json
{
  "is_salary_account": true,
  "confidence": 0.84,
  "scenario": "A",
  "salary_stopped": false,
  "details": {
    "features": {...},
    "transactions": [...]
  }
}
```

✔ Fully transparent
✔ Debuggable
✔ Auditable

## 🧠 Approach Used

We implemented a:

> **Rule-Based Heuristic Model (Pre-ML System)**

### Why this approach?

* No labeled data required
* Fast to build and iterate
* Fully explainable (critical in banking)
* Serves as foundation for ML models

## ⚙️ Architecture (MVP)

```
CSV / Transaction Data
        ↓
Parser Service
        ↓
Feature Engineering
        ↓
Salary Detection Engine
        ↓
Scenario Engine (A/B/C)
        ↓
API Layer (FastAPI + Swagger)
```

## 📊 Reliability (MVP Assessment)

| Capability               | Status           |
| ------------------------ | ---------------- |
| Monthly salary detection | ✅ High           |
| Weekly salary detection  | ✅ Good           |
| False positives          | ⚠ Medium         |
| Freelancer detection     | ⚠ Improving      |
| Edge cases               | ⚠ Needs ML later |

👉 Estimated accuracy: **~75–80% (MVP stage)**

## ⚠️ Known Limitations

* Sensitive to noisy transaction narration
* Freelancers / gig workers may be misclassified
* Dual income sources need refinement
* Limited data (2 months) reduces confidence

## 🔄 Future Enhancements (Phase 2+)

* ML-based classification (Logistic Regression / XGBoost)
* NLP for transaction narration (BERT / TF-IDF)
* Hybrid system (Rules + ML)
* Real-time streaming (Kafka-based)
* Feedback loop for continuous learning

## 🚀 Business Impact

This engine enables:

* Targeted customer engagement
* Retention strategies (Scenario B)
* Churn prevention (Scenario C)
* Personalized financial nudges


## 🧩 Tech Stack

* Python
* FastAPI
* NumPy
* CSV-based dataset (MVP)


## 📌 Summary

We successfully built a **scalable, explainable salary intelligence system** that:

* Detects salary behavior
* Classifies user patterns
* Identifies churn risk