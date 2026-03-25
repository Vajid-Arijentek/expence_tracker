# -*- coding: utf-8 -*-
"""
Scheduled Tasks for Expense Tracker
"""

import frappe
from frappe import _
from frappe.utils import getdate, add_to_date, nowdate, format_datetime
import datetime

def send_daily_summary():
	"""
	Send daily expense summary to users
	Scheduled to run daily
	"""
	today = nowdate()

	# Get today's expenses
	expenses = frappe.db.sql("""
		SELECT expense_category, SUM(amount) as total, COUNT(*) as count
		FROM `tabExpense`
		WHERE expense_date = %s
		AND docstatus = 1
		GROUP BY expense_category
	""", today, as_dict=True)

	if not expenses:
		return

	total_amount = sum(e.total for e in expenses)

	# Build email content
	subject = _("Daily Expense Summary - {0}").format(today)

	message = f"""
	<h2>Daily Expense Summary</h2>
	<p><strong>Date:</strong> {today}</p>
	<p><strong>Total Expenses:</strong> {frappe.format_value(total_amount, dict(fieldtype='Currency'))}</p>
	<p><strong>Transaction Count:</strong> {sum(e.count for e in expenses)}</p>

	<h3>Breakdown by Category:</h3>
	<table border="1" cellpadding="8" style="border-collapse: collapse;">
		<tr>
			<th>Category</th>
			<th>Amount</th>
			<th>Count</th>
		</tr>
	"""

	for exp in expenses:
		message += f"""
		<tr>
			<td>{exp.expense_category}</td>
			<td>{frappe.format_value(exp.total, dict(fieldtype='Currency'))}</td>
			<td>{exp.count}</td>
		</tr>
		"""

	message += "</table>"

	# Send to all users with expense access
	users = frappe.get_all("User", filters={"enabled": 1}, pluck="name")
	for user in users:
		if frappe.has_permission("Expense", "read", user=user):
			frappe.sendmail(
				recipients=[user],
				subject=subject,
				message=message,
				reference_doctype="Expense",
				reference_name="Daily Summary"
			)

def send_monthly_report():
	"""
	Send monthly expense report
	Scheduled to run monthly
	"""
	today = getdate()
	first_day = today.replace(day=1)
	last_day = add_to_date(first_day, months=1, days=-1)

	# Get month's expenses by category
	expenses = frappe.db.sql("""
		SELECT expense_category, SUM(amount) as total, COUNT(*) as count
		FROM `tabExpense`
		WHERE expense_date BETWEEN %s AND %s
		AND docstatus = 1
		GROUP BY expense_category
		ORDER BY total DESC
	""", (first_day, last_day), as_dict=True)

	if not expenses:
		return

	total_amount = sum(e.total for e in expenses)

	# Build email content
	subject = _("Monthly Expense Report - {0}").format(today.strftime("%B %Y"))

	message = f"""
	<h2>Monthly Expense Report</h2>
	<p><strong>Period:</strong> {first_day} to {last_day}</p>
	<p><strong>Total Expenses:</strong> {frappe.format_value(total_amount, dict(fieldtype='Currency'))}</p>
	<p><strong>Total Transactions:</strong> {sum(e.count for e in expenses)}</p>

	<h3>Breakdown by Category:</h3>
	<table border="1" cellpadding="8" style="border-collapse: collapse;">
		<tr>
			<th>Category</th>
			<th>Amount</th>
			<th>Count</th>
			<th>% of Total</th>
		</tr>
	"""

	for exp in expenses:
		percentage = (exp.total / total_amount * 100) if total_amount > 0 else 0
		message += f"""
		<tr>
			<td>{exp.expense_category}</td>
			<td>{frappe.format_value(exp.total, dict(fieldtype='Currency'))}</td>
			<td>{exp.count}</td>
			<td>{percentage:.1f}%</td>
		</tr>
		"""

	message += "</table>"

	# Send to all users with expense access
	users = frappe.get_all("User", filters={"enabled": 1}, pluck="name")
	for user in users:
		if frappe.has_permission("Expense", "read", user=user):
			frappe.sendmail(
				recipients=[user],
				subject=subject,
				message=message,
				reference_doctype="Expense",
				reference_name="Monthly Report"
			)
