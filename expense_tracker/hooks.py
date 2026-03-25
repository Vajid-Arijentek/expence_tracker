# -*- coding: utf-8 -*-
"""
Expense Tracker Application Hooks
"""

app_name = "expense_tracker"
app_title = "Expense Tracker"
app_publisher = "Your Company"
app_description = "Simple Daily Expense Tracking Application"
app_version = "0.0.1"
app_icon = "octicon octicon-file-text"
app_color = "grey"
app_email = "support@example.com"
app_license = "MIT"

# Includes
includes = [
]

# Javascript
js = {
	"expense": [
		"public/js/expense_tracker.js"
	]
}

# CSS
css = [
	"public/css/expense_tracker.css"
]

# Website
website_route_rules = [
	{"from_route": "/expenses", "to_route": "expense_tracker"}
]

# DocType Events
doc_events = {
	"Expense": {
		"validate": "expense_tracker.expense_events.validate_expense",
		"on_submit": "expense_tracker.expense_events.on_submit_expense",
		"on_cancel": "expense_tracker.expense_events.on_cancel_expense"
	}
}

# Scheduled Tasks
scheduler_events = {
	"all": [
		"daily": [
			"expense_tracker.tasks.send_daily_summary",
		],
		"monthly": [
			"expense_tracker.tasks.send_monthly_report",
		]
	]
}

# Permissions
# Permissions are managed through the standard Frappe permissions system

# Notification Configurations
notification_config = "expense_tracker.notifications.get_notification_config"
