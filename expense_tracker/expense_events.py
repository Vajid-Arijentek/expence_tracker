# -*- coding: utf-8 -*-
"""
Expense DocType Event Handlers
"""

import frappe
from frappe import _

def validate_expense(doc, method):
	"""Validate expense before save"""
	if doc.amount and doc.amount <= 0:
		frappe.throw(_("Amount must be greater than zero"))

	if not doc.expense_category:
		frappe.throw(_("Category is required"))

def on_submit_expense(doc, method):
	"""Handle expense submission"""
	# Log the expense submission
	frappe.msgprint(_("Expense {0} submitted successfully").format(doc.name))

	# Check if budget is exceeded
	check_budget_alert(doc)

def on_cancel_expense(doc, method):
	"""Handle expense cancellation"""
	frappe.msgprint(_("Expense {0} cancelled").format(doc.name))

def check_budget_alert(doc):
	"""Check if budget limit is exceeded for the category"""
	try:
		from expense_tracker.api import get_budget_status

		status = get_budget_status(doc.expense_category)

		if status.get("status") == "Over Budget":
			frappe.msgprint(
				_("Warning: Budget exceeded for category {0}! "
				  "Spent: {1}, Budget: {2}").format(
					doc.expense_category,
					status["spent"],
					status["budget_limit"]
				),
				indicator="red",
				alert=True
			)
		elif status.get("percentage_used", 0) > 80:
			frappe.msgprint(
				_("Notice: You've used {0}% of your budget for {1}").format(
					int(status["percentage_used"]),
					doc.expense_category
				),
				indicator="orange",
				alert=True
			)
	except Exception as e:
		# Don't fail if budget check fails
		pass
