# Python — Personal Expense Tracker

Desktop expense management app built with **Python, Tkinter, CSV, Pandas, and Matplotlib**. This repository contains **fictional sample financial data**.

## Features
- Add, update, delete, and filter income / expense transactions
- Persist records in `data/transactions.csv`
- View income, expense, and balance totals in LKR
- See bar and pie charts showing spending by category
- Validate dates, numbers, and amounts

## Folder structure
```text
python-expense-tracker/
├── main.py
├── expense_manager.py
├── dashboard.py
├── requirements.txt
├── README.md
├── data/
│   └── transactions.csv
└── screenshots/
```

## How to run
1. Install Python 3 with Tkinter (included in common Windows Python installations).
2. Open this folder in VS Code.
3. In the VS Code terminal, install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
4. Start the app:
   ```bash
   python main.py
   ```
   On Windows, you can use `py` instead of `python` if needed.

## How to use
- Enter a date in `YYYY-MM-DD` format, select a type, and enter a category and positive amount.
- Click **Add** to save a transaction.
- Select a row and click **Update Selected** or **Delete Selected**.
- Choose **Income** or **Expense** in the Filter dropdown.
- Click **Show Charts** to inspect expenses by category.

## Learning goals
Functions, validation, CSV file handling, CRUD, Tkinter event handling, Pandas `groupby`, and Matplotlib charts.
