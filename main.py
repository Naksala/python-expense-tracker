"""Tkinter GUI for the Personal Expense Tracker. Run: python main.py"""
import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

from expense_manager import (add_transaction, delete_transaction, load_transactions,
                             update_transaction)
from dashboard import show_charts, totals


class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Personal Expense Tracker | Python Project 03')
        self.root.geometry('1050x680')
        self.selected_id = None
        self.date_var = tk.StringVar(value=date.today().isoformat())
        self.type_var = tk.StringVar(value='Expense')
        self.category_var = tk.StringVar(value='Food')
        self.amount_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.filter_var = tk.StringVar(value='All')
        self.summary_var = tk.StringVar()
        self.build_ui()
        self.refresh()

    def build_ui(self):
        outer = ttk.Frame(self.root, padding=18)
        outer.pack(fill='both', expand=True)
        ttk.Label(outer, text='Personal Expense Tracker', font=('Arial', 21, 'bold')).pack(anchor='w')
        ttk.Label(outer, text='Manage income and expenses in LKR').pack(anchor='w', pady=(0, 12))
        form = ttk.LabelFrame(outer, text='Transaction Details', padding=12)
        form.pack(fill='x')
        fields = [ ('Date (YYYY-MM-DD)', self.date_var), ('Category', self.category_var),
                   ('Amount (LKR)', self.amount_var), ('Description', self.description_var)]
        ttk.Label(form, text='Type').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        ttk.Combobox(form, textvariable=self.type_var, values=['Income', 'Expense'],
                     state='readonly', width=20).grid(row=1, column=0, sticky='ew', padx=5)
        for col, (label, variable) in enumerate(fields, start=1):
            ttk.Label(form, text=label).grid(row=0, column=col, sticky='w', padx=5, pady=5)
            ttk.Entry(form, textvariable=variable, width=23).grid(row=1, column=col, sticky='ew', padx=5)
            form.columnconfigure(col, weight=1)
        actions = ttk.Frame(outer)
        actions.pack(fill='x', pady=12)
        for text, callback in [('Add', self.add), ('Update Selected', self.update),
                               ('Delete Selected', self.delete), ('Clear', self.clear),
                               ('Show Charts', self.charts)]:
            ttk.Button(actions, text=text, command=callback).pack(side='left', padx=(0, 9))
        ttk.Label(actions, text='Filter:').pack(side='left', padx=(25, 5))
        ttk.Combobox(actions, textvariable=self.filter_var, state='readonly', width=12,
                     values=['All', 'Income', 'Expense']).pack(side='left')
        self.filter_var.trace_add('write', lambda *_: self.refresh())
        ttk.Label(outer, textvariable=self.summary_var, font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0, 12))
        table_frame = ttk.Frame(outer)
        table_frame.pack(fill='both', expand=True)
        columns = ('date', 'type', 'category', 'amount', 'description')
        self.table = ttk.Treeview(table_frame, columns=columns, show='headings', selectmode='browse')
        for col, width in zip(columns, (130, 110, 160, 120, 350)):
            self.table.heading(col, text=col.title())
            self.table.column(col, width=width, anchor='w')
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.table.bind('<<TreeviewSelect>>', self.select_row)
        ttk.Label(outer, text='Tip: Select a row to update or delete it. Data is saved to data/transactions.csv.').pack(anchor='w', pady=(10, 0))

    def refresh(self):
        transactions = load_transactions()
        for item in self.table.get_children():
            self.table.delete(item)
        for record in sorted(transactions, key=lambda t: t['date'], reverse=True):
            if self.filter_var.get() not in ('All', record['type']):
                continue
            self.table.insert('', 'end', iid=record['id'], values=(
                record['date'], record['type'], record['category'],
                f"{float(record['amount']):,.2f}", record['description']))
        income, expenses, balance = totals(transactions)
        self.summary_var.set(f'Income: LKR {income:,.2f}     Expenses: LKR {expenses:,.2f}     Balance: LKR {balance:,.2f}')

    def values(self):
        return (self.date_var.get().strip(), self.type_var.get(), self.category_var.get(),
                self.amount_var.get().strip(), self.description_var.get())

    def add(self):
        try:
            add_transaction(*self.values())
        except ValueError as error:
            messagebox.showerror('Invalid Transaction', str(error))
            return
        self.clear()
        self.refresh()

    def update(self):
        if not self.selected_id:
            messagebox.showinfo('Select a Transaction', 'Please select a row first.')
            return
        try:
            update_transaction(self.selected_id, *self.values())
        except ValueError as error:
            messagebox.showerror('Unable to Update', str(error))
            return
        self.clear()
        self.refresh()

    def delete(self):
        if not self.selected_id:
            messagebox.showinfo('Select a Transaction', 'Please select a row first.')
            return
        if messagebox.askyesno('Confirm Delete', 'Delete selected transaction?'):
            delete_transaction(self.selected_id)
            self.clear()
            self.refresh()

    def select_row(self, _event):
        selected = self.table.selection()
        if not selected:
            return
        self.selected_id = selected[0]
        record = next((t for t in load_transactions() if t['id'] == self.selected_id), None)
        if record:
            self.date_var.set(record['date'])
            self.type_var.set(record['type'])
            self.category_var.set(record['category'])
            self.amount_var.set(record['amount'])
            self.description_var.set(record['description'])

    def clear(self):
        self.selected_id = None
        self.date_var.set(date.today().isoformat())
        self.type_var.set('Expense')
        self.category_var.set('Food')
        self.amount_var.set('')
        self.description_var.set('')
        self.table.selection_remove(self.table.selection())

    def charts(self):
        if not show_charts(load_transactions()):
            messagebox.showinfo('No Expense Data', 'Add an expense to view charts.')


if __name__ == '__main__':
    root = tk.Tk()
    ExpenseTrackerApp(root)
    root.mainloop()
