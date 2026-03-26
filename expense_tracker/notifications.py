# -*- coding: utf-8 -*-
"""
Notification Configuration for Expense Tracker
"""

import frappe

def get_notification_config():
	"""
	Return notification configuration for expense tracker
	"""
	return {
		"for_doctype": {
			"Expense": {
				"Expense": {
					"text": _("New Expense: {0}"),
					"alert_text": _("Amount: {0}"),
				}
			}
		}
	}
