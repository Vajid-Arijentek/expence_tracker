# -*- coding: utf-8 -*-
import frappe
from frappe import _

@frappe.whitelist()
def get_monthly_total(date=None):
	"""Get total expenses for a given month"""
	if not date:
		date = frappe.utils.today()

	year, month = frappe.utils.get_year_month(date)
	total = frappe.db.sql("""
		SELECT SUM(amount)
		FROM `tabExpense`
		WHERE YEAR(expense_date) = %s
		AND MONTH(expense_date) = %s
		AND docstatus = 1
	""", (year, month))[0][0]

	return total or 0

@frappe.whitelist()
def get_category_total(category):
	"""Get total expenses for a category"""
	total = frappe.db.sql("""
		SELECT SUM(amount)
		FROM `tabExpense`
		WHERE expense_category = %s
		AND docstatus = 1
		AND MONTH(expense_date) = MONTH(CURDATE())
		AND YEAR(expense_date) = YEAR(CURDATE())
	""", category)[0][0]

	return total or 0

@frappe.whitelist()
def get_expense_summary(start_date, end_date):
	"""Get expense summary by category"""
	data = frappe.db.sql("""
		SELECT
			exp.expense_category,
			COALESCE(SUM(exp.amount), 0) as total,
			COUNT(exp.name) as count
		FROM `tabExpense` exp
		WHERE exp.expense_date BETWEEN %s AND %s
		AND exp.docstatus = 1
		GROUP BY exp.expense_category
		ORDER BY total DESC
	""", (start_date, end_date), as_dict=True)

	return data

@frappe.whitelist()
def mark_approved(expense):
	"""Mark expense as approved"""
	doc = frappe.get_doc("Expense", expense)
	if doc.docstatus != 1:
		frappe.throw(_("Only submitted expenses can be approved"))
	doc.status = "Approved"
	doc.save()
	return {"status": "success"}

@frappe.whitelist()
def get_daily_expenses(date):
	"""Get all expenses for a specific date"""
	expenses = frappe.db.get_all("Expense",
		filters={"expense_date": date, "docstatus": 1},
		fields=["name", "expense_category", "amount", "description", "payment_method"],
		order_by="creation desc"
	)
	return expenses

@frappe.whitelist()
def get_budget_status(category):
	"""Check budget status for a category"""
	category_doc = frappe.get_doc("Expense Category", category)
	if not category_doc.budget_limit:
		return {"status": "No budget set"}

	year, month = frappe.utils.get_year_month(frappe.utils.today())
	spent = frappe.db.sql("""
		SELECT SUM(amount)
		FROM `tabExpense`
		WHERE expense_category = %s
		AND YEAR(expense_date) = %s
		AND MONTH(expense_date) = %s
		AND docstatus = 1
	""", (category, year, month))[0][0] or 0

	remaining = category_doc.budget_limit - spent
	percentage_used = (spent / category_doc.budget_limit) * 100 if category_doc.budget_limit > 0 else 0

	return {
		"budget_limit": category_doc.budget_limit,
		"spent": spent,
		"remaining": remaining,
		"percentage_used": percentage_used,
		"status": "Over Budget" if remaining < 0 else "Under Budget"
	}
