# Expense Tracker

[![Frappe Framework](https://img.shields.io/badge/Frappe-v15-blue)](https://frappeframework.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B--3.11-yellow)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](license.txt)

A comprehensive daily expense tracking application built for the Frappe Framework v15.

## Overview

Expense Tracker is a Frappe application that helps individuals and organizations track daily expenses with categorization, budget management, and automated reporting features.

## Version

**0.0.1** - Frappe v15 Compatible

## License

MIT License - Copyright (c) 2026 Expense Tracker

## Compatibility

| Component | Version |
|-----------|---------|
| Frappe Framework | v15.x |
| ERPNext | Not required (standalone app) |
| Python | 3.10 - 3.11 |
| MariaDB | 10.6+ |
| Frappe Docker | ✅ Compatible |

## Features

- **Expense Tracking**: Record daily expenses with detailed information
- **Category Management**: Organize expenses by custom categories
- **Budget Management**: Set monthly budget limits per category
- **Receipt Attachments**: Attach receipt images to expenses
- **Status Workflow**: Track expenses through Pending, Verified, Approved, or Rejected states
- **Payment Methods**: Support for Cash, Credit Card, Debit Card, Bank Transfer, UPI, Digital Wallet, and Other
- **Dashboard**: Real-time summary with daily, monthly, and yearly totals
- **CSV Export**: Export expense data to CSV format
- **Email Notifications**: Automated daily summaries and monthly reports
- **Budget Alerts**: Warnings when budget limits are approached or exceeded
- **Quick Add**: Fast expense entry through dialog interface
- **REST API**: Full API endpoints for integration

## Requirements

- Frappe Framework v15.x
- Python 3.10 or 3.11
- MariaDB 10.6+ (or MySQL 8.0+)
- Node.js 18+ (for bench build)

## Installation

### Using Frappe Bench

```bash
cd /path/to/frappe-bench

# Option 1: Clone from GitHub (version-15 branch)
bench get-app https://github.com/Vajid-Arijentek/expence_tracker.git --branch version-15

# Option 2: Clone main branch (also v15 compatible)
bench get-app https://github.com/Vajid-Arijentek/expence_tracker.git

# Install the app
bench install-app expense_tracker

# Build and restart
bench build
bench restart
```

### Using frappe_docker

Add to your `compose.yaml` or install via bench:

```bash
# Inside your frappe_docker container
bench get-app https://github.com/Vajid-Arijentek/expence_tracker.git --branch version-15
bench install-app expense_tracker
bench new-site your-site.local
bench --site your-site.local install-app expense_tracker
```

### Development Setup

```bash
# Clone for development
git clone https://github.com/Vajid-Arijentek/expence_tracker.git
cd expence_tracker

# Link to existing bench
bench get-app expense_tracker /path/to/expence_tracker
```

## Project Structure

```
expense_tracker/
├── expense_tracker/              # Main application package
│   ├── __init__.py               # Package initialization (v0.0.1)
│   ├── hooks.py                  # Application hooks and configuration
│   ├── expense_events.py         # DocType event handlers
│   ├── tasks.py                  # Scheduled tasks
│   ├── notifications.py          # Notification configuration
│   │
│   ├── api/                      # API endpoints
│   │   ├── __init__.py           # API helper functions
│   │   └── expense_api.py        # REST API for expense operations
│   │
│   ├── config/                   # Configuration files
│   ├── public/                   # Public assets
│   │   ├── js/
│   │   │   └── expense_tracker.js  # Client-side JavaScript
│   │   └── css/
│   │       └── expense_tracker.css # Stylesheets
│   │
│   └── modules/                  # Application modules
│       └── expenses/             # Expenses module
│           └── doctype/          # DocTypes
│               ├── expense/      # Expense DocType
│               │   ├── expense.json
│               │   ├── expense.py
│               │   ├── expense.js
│               │   └── templates/
│               │       └── expense.html
│               └── expense_category/  # Expense Category DocType
│                   ├── expense_category.json
│                   └── expense_category.py
│
├── modules.txt                   # Frappe modules list
├── setup.py                      # Python package configuration
├── pyproject.toml                # Modern Python packaging
├── requirements.txt              # Python dependencies (Frappe v15)
├── license.txt                   # MIT License
└── README.md                     # This file
```

## DocTypes

### Expense
Main document for recording individual expenses with the following fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Naming Series | Select | Yes | Auto-generated ID (EXP-.YYYY.-.####) |
| Date | Date | Yes | Expense date (default: Today) |
| Category | Link | Yes | Reference to Expense Category |
| Amount | Currency | Yes | Expense amount |
| Description | Data | No | Short description (max 255 chars) |
| Payment Method | Select | No | Cash, Credit Card, Debit Card, etc. |
| Vendor/Payee | Data | No | Name of vendor or payee |
| Status | Select | Auto | Pending, Verified, Approved, Rejected |
| Receipt Attached | Check | No | Indicates if receipt is attached |
| Receipt Image | Attach Image | No | Image of the receipt |
| Notes | Text | No | Additional notes |

### Expense Category
Categories for organizing expenses:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Category Name | Data | Yes | Unique category name |
| Description | Text | No | Category description |
| Monthly Budget Limit | Currency | No | Budget cap for this category |
| Is Active | Check | No | Enable/disable category |
| Color | Color | No | Visual indicator for UI |

## API Endpoints

### GET `/api/method/expense_tracker.api.get_expenses`
Retrieve expenses with optional filters.

**Query Parameters:**
```json
{
  "from_date": "2026-01-01",    // Optional: Start date filter
  "to_date": "2026-12-31",      // Optional: End date filter
  "category": "Food",           // Optional: Category filter
  "status": "Approved"          // Optional: Status filter
}
```

### POST `/api/method/expense_tracker.api.create_expense`
Create a new expense record.

**Request Body:**
```json
{
  "expense_date": "2026-03-27",
  "expense_category": "Food",
  "amount": 25.50,
  "description": "Lunch",
  "payment_method": "Cash",
  "vendor": "Restaurant Name"
}
```

### GET `/api/method/expense_tracker.api.get_dashboard_data`
Get dashboard summary statistics.

**Returns:**
```json
{
  "today_total": 150.00,
  "month_total": 2500.00,
  "year_total": 15000.00,
  "pending_count": 3,
  "category_breakdown": [
    {"expense_category": "Food", "total": 500.00},
    {"expense_category": "Transport", "total": 300.00}
  ]
}
```

### GET `/api/method/expense_tracker.api.export_to_csv`
Export expenses to CSV format.

**Query Parameters:**
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)

### GET `/api/method/expense_tracker.api.get_budget_status`
Check budget status for a category.

**Query Parameters:**
- `category`: Expense category name

## Scheduled Tasks

| Task | Frequency | Description |
|------|-----------|-------------|
| `send_daily_summary` | Daily | Sends email with daily expense breakdown |
| `send_monthly_report` | Monthly | Sends comprehensive monthly expense report |

## Event Handlers

### Expense DocType Events

- **`validate`**: Validates amount > 0 and category is required
- **`on_submit`**: Logs submission and checks budget alerts
- **`on_cancel`**: Handles expense cancellation

### Budget Alerts

When submitting an expense, the system automatically:
- Warns when budget is exceeded (red alert)
- Notifies when 80%+ of budget is used (orange warning)

## Permissions

| Role | Create | Read | Write | Submit | Delete |
|------|--------|------|-------|--------|--------|
| System Manager | Yes | Yes | Yes | Yes | Yes |
| All | Yes | Yes | Yes | No | No |

## Development

### Running Bench Commands

```bash
# Get shell in bench container (frappe_docker)
docker compose exec backend bash

# Install dependencies
bench pip install -r apps/expense_tracker/requirements.txt

# Build assets
bench build --app expense_tracker

# Restart bench
bench restart
```

## Changelog

### v0.0.1 (2026-03-27)
- Initial release for Frappe v15
- Expense tracking with categories
- Budget management per category
- REST API endpoints
- CSV export functionality
- Scheduled reports
- Frappe Docker compatibility

## Application Configuration (hooks.py)

The application is configured through `hooks.py` with:
- Document events mapping
- Scheduled tasks configuration
- JavaScript/CSS asset loading
- Website route rules
- Notification settings

## Support

For support, email: support@example.com

## Repository

- **GitHub**: https://github.com/Vajid-Arijentek/expence_tracker
- **Issue Tracker**: https://github.com/Vajid-Arijentek/expence_tracker/issues
