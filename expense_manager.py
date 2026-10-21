"""CSV storage and validation for the Personal Expense Tracker."""
import csv
from datetime import datetime
from pathlib import Path
from uuid import uuid4

DATA_FILE = Path(__file__).resolve().parent / 'data' / 'transactions.csv'
FIELDS = ['id', 'date', 'type', 'category', 'amount', 'description']
TYPES = ('Income', 'Expense')


def ensure_file():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        with DATA_FILE.open('w', newline='', encoding='utf-8') as file:
            csv.DictWriter(file, fieldnames=FIELDS).writeheader()


def load_transactions():
    ensure_file()
    with DATA_FILE.open('r', newline='', encoding='utf-8') as file:
        return list(csv.DictReader(file))


def save_transactions(transactions):
    ensure_file()
    with DATA_FILE.open('w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(transactions)


def validate_transaction(date, kind, category, amount, description=''):
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError as exc:
        raise ValueError('Date must be a valid YYYY-MM-DD date.') from exc
    if kind not in TYPES:
        raise ValueError('Type must be Income or Expense.')
    category = category.strip()
    if not category:
        raise ValueError('Category cannot be empty.')
    try:
        amount = float(amount)
    except (ValueError, TypeError) as exc:
        raise ValueError('Amount must be a number.') from exc
    if not (0 < amount < float('inf')):
        raise ValueError('Amount must be a positive finite number.')
    return {'date': date, 'type': kind, 'category': category,
            'amount': f'{amount:.2f}', 'description': description.strip()}


def add_transaction(date, kind, category, amount, description=''):
    record = validate_transaction(date, kind, category, amount, description)
    record['id'] = uuid4().hex[:12]
    transactions = load_transactions()
    transactions.append(record)
    save_transactions(transactions)
    return record


def update_transaction(transaction_id, date, kind, category, amount, description=''):
    new = validate_transaction(date, kind, category, amount, description)
    transactions = load_transactions()
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transaction.update(new)
            save_transactions(transactions)
            return transaction
    raise ValueError('Transaction not found.')


def delete_transaction(transaction_id):
    transactions = load_transactions()
    updated = [t for t in transactions if t['id'] != transaction_id]
    if len(updated) == len(transactions):
        raise ValueError('Transaction not found.')
    save_transactions(updated)
