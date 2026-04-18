# Responsibilities: Detect periodicity, Score salary likelihood, Return classification

# Score based on:
# Feature	                 Why
# interval_std	 ->  	salary is periodic
# amount_std	 ->  	salary is stable
# count	         ->  	repeated pattern
# interval_mean	 ->  determines weekly/monthly

from app.services.feature_engineering import (
    extract_credit_transactions,
    group_by_sender,
    compute_features
)


def detect_salary_account(transactions):

    credits = extract_credit_transactions(transactions)
    sender_groups = group_by_sender(credits)

    best_candidate = None
    best_score = 0

    for sender, txns in sender_groups.items():

        features = compute_features(txns)

        if features is None:
            continue
        if not is_probable_salary(features):
            continue
        if sender == "BUSINESS":
            continue 
        score = calculate_score(features)

        print(f"[DEBUG] Sender={sender}, Score={score}, Features={features}")

        if score > best_score:
            best_score = score
            best_candidate = {
                "sender": sender,
                "features": features,
                "score": score,
                "transactions": [
                    {
                        "date": t.date.strftime("%Y-%m-%d"),
                        "amount": t.amount,
                        "type": t.type,
                        "details": t.details,
                        "category": t.category
                    }
                    for t in txns
                ]
            }
    

    if best_candidate is None:
        return {
            "is_salary_account": False,
            "confidence": 0,
            "confidence_level": "LOW"
        }

    if best_score > 0.35:
        confidence = float(round(best_score, 2))
        return {
            "is_salary_account": True,
            "confidence": confidence,
            "confidence_level": get_confidence_level(confidence),
            "details": best_candidate
        }

    confidence = float(round(best_score, 2))
    return {
        "is_salary_account": False,
        "confidence": confidence,
        "confidence_level": get_confidence_level(confidence)
    }

def is_probable_salary(features):
    interval_mean = features["interval_mean"]
    interval_std = features["interval_std"]
    amount_std = features["amount_std"]
    count = features["count"]

    # ✅ RELAXED RULES
    is_periodic = (
        (24 <= interval_mean <= 35) or
        (5 <= interval_mean <= 9) or
        (12 <= interval_mean <= 18)
    )

    is_stable_amount = amount_std < 10000   # 🔥 increased from 5000
    has_repetition = count >= 2

    return is_periodic and is_stable_amount and has_repetition

def calculate_score(features):

    interval_std = features["interval_std"]
    amount_std = features["amount_std"]
    amount_mean = features["amount_mean"]  
    count = features["count"]

    # Normalize scores (lower std = better)
    time_score = 1 / (1 + interval_std)
    amount_score = 1 / (1 + (amount_std / amount_mean)) 

    salary_boost = 1 if amount_mean > 30000 else 0

    count_score = min(count / 5, 1)

    final_score = (
        0.6 * time_score +
        0.25 * amount_score +
        0.15 * count_score +
        0.1 * salary_boost
    )

    final_score = min(final_score, 1.0)
    return final_score

def get_confidence_level(score):
    if score >= 0.8:
        return "HIGH"
    elif score >= 0.5:
        return "MEDIUM"
    else:
        return "LOW"