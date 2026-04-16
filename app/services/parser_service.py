# Convert CSV → objects

import csv
from datetime import datetime
from app.models.transaction import Transaction


def load_transactions(file_path: str):
    transactions = []

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                txn = Transaction(
                    date=datetime.strptime(row["Date"], "%Y-%m-%d"),
                    customer_id=row["CustomerId"],
                    details=row["Transaction Details"],
                    type=row["Type"] if row["Type"] else "",
                    amount=float(row["Amount"]),
                    balance=float(row["Balance"]),
                    category=row["Category"] if row["Category"] else ""
                )
                transactions.append(txn)

            except Exception as e:
                print(f"Skipping row due to error: {row}, Error: {e}")

    return transactions

def group_by_customer(transactions):
    from collections import defaultdict
    customer_map = defaultdict(list)

    for txn in transactions:
        customer_map[txn.customer_id].append(txn)
        

    return customer_map