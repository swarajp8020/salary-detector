# Extract: credit transactions, date intervals, amount variance, sender extraction
# Only CREDIT transactions, Group by sender, Extract: dates, amounts, intervals
#  extracted:
# interval_mean  → salary frequency
# interval_std   → consistency
# amount_mean    → salary level
# amount_std     → stability
# count          → repetition

from collections import defaultdict
import numpy as np


def extract_credit_transactions(transactions):
    return [
        t for t in transactions
        if t.type == "Credit" and t.amount >= 3000
    ]


def group_by_sender(transactions):
    sender_map = defaultdict(list)

    for txn in transactions:
        sender = extract_sender(txn.details)
        sender_map[sender].append(txn)

    return sender_map


def extract_sender(details):
    details = details.upper()
    parts = details.split("/")

    if len(parts) >= 2:
        sender = parts[1]
        words = sender.split()

        sender = " ".join(words[:2])  # better than words[0]

        if sender.replace(" ", "").isdigit():
            return f"ANON_{sender.replace(' ', '')}"

        return sender.strip()

    return details


def compute_features(txns):
    # ✅ Step 1: sort transactions
    txns = sorted(txns, key=lambda x: x.date)

    # ✅ Step 2: merge same-day credits (FIXED POSITION)
    date_amount_map = defaultdict(float)

    for t in txns:
        date_amount_map[t.date] += t.amount

    merged_dates = sorted(date_amount_map.keys())
    merged_amounts = [date_amount_map[d] for d in merged_dates]

    # ✅ Step 3: convert to numeric
    dates = [d.toordinal() for d in merged_dates]
    amounts = merged_amounts

    # ✅ Step 4: minimum data check
    if len(dates) < 2:
        return None

    # ✅ Step 5: compute intervals
    intervals = np.diff(dates)

    return {
        "interval_mean": float(np.mean(intervals)),
        "interval_std": float(np.std(intervals)),
        "amount_mean": float(np.mean(amounts)),
        "amount_std": float(np.std(amounts)),
        "count": len(merged_dates)  # ✅ important: use merged count
    }