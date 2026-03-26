# -*- coding: utf-8 -*-
from frappe.model.document import Document
import frappe

class Expense(Document):
	def validate(self):
		self.validate_amount()
		self.set_status()

	def validate_amount(self):
		if self.amount and self.amount <= 0:
			frappe.throw("Amount must be greater than zero")

	def set_status(self):
		if self.docstatus == 0:
			self.status = "Pending"
		elif self.docstatus == 1:
			self.status = "Verified"
		elif self.docstatus == 2:
			self.status = "Rejected"

	def on_submit(self):
		self.status = "Verified"

	def on_cancel(self):
		self.status = "Rejected"

	def on_update_after_submit(self):
		"""Handle updates after submission"""
		pass
