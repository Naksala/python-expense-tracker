"""Pandas summaries and Matplotlib charts for expense tracking."""
import pandas as pd
from matplotlib import pyplot as plt


def to_dataframe(transactions):
    columns = ['id', 'date', 'type', 'category', 'amount', 'description']
    frame = pd.DataFrame(transactions, columns=columns)
    if not frame.empty:
        frame['amount'] = pd.to_numeric(frame['amount'], errors='coerce').fillna(0)
        frame['date'] = pd.to_datetime(frame['date'], errors='coerce')
    return frame


def totals(transactions):
    frame = to_dataframe(transactions)
    if frame.empty:
        return 0.0, 0.0, 0.0
    income = float(frame.loc[frame['type'] == 'Income', 'amount'].sum())
    expenses = float(frame.loc[frame['type'] == 'Expense', 'amount'].sum())
    return income, expenses, income - expenses


def show_charts(transactions):
    frame = to_dataframe(transactions)
    expenses = frame.loc[frame['type'] == 'Expense'] if not frame.empty else frame
    if expenses.empty:
        return False
    grouped = expenses.groupby('category')['amount'].sum().sort_values(ascending=False)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    grouped.plot(kind='bar', ax=axes[0])
    axes[0].set_title('Expenses by Category (LKR)')
    axes[0].set_xlabel('Category')
    axes[0].set_ylabel('Amount (LKR)')
    axes[0].tick_params(axis='x', rotation=35)
    axes[1].pie(grouped.values, labels=grouped.index, autopct='%1.1f%%', startangle=90)
    axes[1].set_title('Expense Share')
    fig.tight_layout()
    plt.show()
    return True
