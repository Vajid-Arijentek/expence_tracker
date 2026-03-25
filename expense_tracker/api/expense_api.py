# -*- coding: utf-8 -*-
"""
Expense Tracker API Endpoints

This module provides REST API endpoints for the expense tracker application.
"""

import frappe
from frappe import _
from frappe.utils import getdate, add_to_date, nowdate
import json

@frappe.whitelist(methods=['GET'])
def get_expenses(filters=None):
	"""
	Get expenses with optional filters

	Args:
		filters: JSON string with filter criteria
			- from_date: Start date
			- to_date: End date
			- category: Expense category
			- status: Document status

	Returns:
		List of expense documents
	"""
	if isinstance(filters, str):
		filters = json.loads(filters) if filters else {}

	query = frappe.db.get_list("Expense",
		fields=["name", "expense_date", "expense_category", "amount",
				"description", "payment_method", "vendor", "status", "docstatus"],
		filters={"docstatus": ("!=", 2)},
		order_by="expense_date desc, creation desc"
	)

	# Apply additional filters
	if filters:
		if filters.get("from_date"):
			query = [x for x in query if x["expense_date"] >= filters["from_date"]]
		if filters.get("to_date"):
			query = [x for x in query if x["expense_date"] <= filters["to_date"]]
		if filters.get("category"):
			query = [x for x in query if x["expense_category"] == filters["category"]]
		if filters.get("status"):
			query = [x for x in query if x["status"] == filters["status"]]

	return query

@frappe.whitelist(methods=['POST'])
def create_expense(data):
	"""
	Create a new expense record

	Args:
		data: Expense data as JSON string

	Returns:
		Created expense document
	"""
	if isinstance(data, str):
		data = json.loads(data)

	expense = frappe.new_doc("Expense")
	expense.update(data)
	expense.insert()

	return expense.as_dict()

@frappe.whitelist(methods=['GET'])
def get_dashboard_data():
	"""
	Get dashboard summary data

	Returns:
		Dictionary with:
		- today_total: Today's expenses
		- month_total: Current month's expenses
		- year_total: Current year's expenses
		- pending_count: Number of pending expenses
		- category_breakdown: Expenses by category
	"""
	today = nowdate()
	year, month = frappe.utils.get_year_month(today)

	today_total = frappe.db.get_value("Expense",
		{"expense_date": today, "docstatus": 1},
		"COALESCE(SUM(amount), 0)")

	month_total = frappe.db.sql("""
		SELECT COALESCE(SUM(amount), 0)
		FROM `tabExpense`
		WHERE MONTH(expense_date) = %s
		AND YEAR(expense_date) = %s
		AND docstatus = 1
	""", (month, year))[0][0]

	year_total = frappe.db.sql("""
		SELECT COALESCE(SUM(amount), 0)
		FROM `tabExpense`
		WHERE YEAR(expense_date) = %s
		AND docstatus = 1
	""", year)[0][0]

	pending_count = frappe.db.count("Expense", {"docstatus": 0})

	category_breakdown = frappe.db.sql("""
		SELECT expense_category, SUM(amount) as total
		FROM `tabExpense`
		WHERE MONTH(expense_date) = %s
		AND YEAR(expense_date) = %s
		AND docstatus = 1
		GROUP BY expense_category
		ORDER BY total DESC
	""", (month, year), as_dict=True)

	return {
		"today_total": today_total or 0,
		"month_total": month_total or 0,
		"year_total": year_total or 0,
		"pending_count": pending_count,
		"category_breakdown": category_breakdown
	}

@frappe.whitelist()
def export_to_csv(start_date, end_date):
	"""
	Export expenses to CSV format

	Args:
		start_date: Start date (YYYY-MM-DD)
		end_date: End date (YYYY-MM-DD)

	Returns:
		CSV formatted string
	"""
	import csv
	from io import StringIO

	expenses = frappe.db.sql("""
		SELECT
			name, expense_date, expense_category, amount,
			description, payment_method, vendor, status
		FROM `tabExpense`
		WHERE expense_date BETWEEN %s AND %s
		AND docstatus = 1
		ORDER BY expense_date
	""", (start_date, end_date), as_dict=True)

	output = StringIO()
	writer = csv.writer(output)

	# Header
	writer.writerow(["ID", "Date", "Category", "Amount", "Description",
					"Payment Method", "Vendor", "Status"])

	# Data
	for exp in expenses:
		writer.writerow([
			exp.name, exp.expense_date, exp.expense_category,
			exp.amount, exp.description or "",
			exp.payment_method or "", exp.vendor or "", exp.status
		])

	return output.getvalue()
