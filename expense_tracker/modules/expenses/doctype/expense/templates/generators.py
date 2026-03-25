# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import frappe

def get_context(context):
	context.parents = [{"name": frappe._("Expenses"), "route": "/expenses"}]
	return context
