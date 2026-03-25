# -*- coding: utf-8 -*-
from frappe.model.document import Document
import frappe

class ExpenseCategory(Document):
	def validate(self):
		self.check_duplicate()

	def check_duplicate(self):
		if self.is_new():
			exists = frappe.db.exists("Expense Category", {"category_name": self.category_name})
			if exists:
				frappe.throw("Category with this name already exists")
