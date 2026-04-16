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
            "confidence": 0
        }

    if best_score > 0.35:
        return {
            "is_salary_account": True,
            "confidence": float(round(best_score, 2)),
            "details": best_candidate
        }

    return {
        "is_salary_account": False,
        "confidence": float(round(best_score, 2))
    }


def calculate_score(features):

    interval_std = features["interval_std"]
    amount_std = features["amount_std"]
    amount_mean = features["amount_mean"]  # ✅ MOVE THIS UP
    count = features["count"]

    # Normalize scores (lower std = better)
    time_score = 1 / (1 + interval_std)
    amount_score = 1 / (1 + (amount_std / amount_mean))  # ✅ now safe

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