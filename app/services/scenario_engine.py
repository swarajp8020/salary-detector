from datetime import datetime, timedelta


def classify_scenario(transactions, salary_details):

    salary_txns = salary_details["transactions"]

    if not salary_txns:
        return "UNKNOWN"

    latest_salary = max(salary_txns, key=lambda x: x["date"])
    latest_date = latest_salary["date"]
    salary_amount = latest_salary["amount"]

    # convert string → date
    from datetime import datetime
    latest_date = datetime.strptime(latest_date, "%Y-%m-%d")

    # define window (48 hours)
    window_end = latest_date + timedelta(days=2)

    debit_sum = 0
    
    for txn in transactions:
        if txn.type == "Debit" and latest_date <= txn.date <= window_end:
            debit_sum += txn.amount

    ratio = debit_sum / salary_amount
    
    # Scenario B: money drained
    if ratio > 0.8:
        return "B"

    # Scenario C: no salary this cycle (we check outside)
    # handled separately

    # Scenario A: normal usage
    return "A"

def detect_salary_stopped(details, txns):

    if not details or "transactions" not in details:
        return False

    salary_txns = details["transactions"]

    # need at least 2 salaries to predict pattern
    if len(salary_txns) < 2:
        return False

    # 🚀 MVP LOGIC (BEST FOR NOW)
    # if only 2 salary entries → assume next one missing → churn
    # If scenario is B (salary drained), DO NOT mark as churn
    if len(salary_txns) == 2:
        latest_salary = salary_txns[-1]["amount"]

        # check if money was used (not abandoned)
        debit_sum = sum(
            txn.amount for txn in txns
            if txn.type == "Debit"
        )

        if debit_sum > 0:
            return False  # active usage → NOT churn

        return True

    # fallback (future safe)
    last_salary_date = max(
        datetime.strptime(t["date"], "%Y-%m-%d").date()
        for t in salary_txns
    )

    interval = details["features"]["interval_mean"]
    expected_next_salary = last_salary_date + timedelta(days=int(interval))

    # use transaction timeline (not system time)
    current_date = max(txn.date for txn in txns).date()

    grace_days = 5

    print(f"[CHURN DEBUG] last={last_salary_date}, expected={expected_next_salary}, current={current_date}")

    if current_date > expected_next_salary + timedelta(days=grace_days):
        return True

    return False