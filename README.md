# Expense Tracker

A simple daily expense tracking application for Frappe Framework.

## Features

- **Expense Tracking**: Log daily expenses with categories, amounts, and details
- **Categories**: Organize expenses into customizable categories
- **Budget Management**: Set monthly budget limits per category
- **Receipt Attachments**: Attach receipt images to expenses
- **Status Tracking**: Track expenses through Pending, Verified, Approved, or Rejected states
- **Dashboard**: View daily, monthly, and yearly expense summaries
- **Reports**: Export expenses to CSV format
- **Email Notifications**: Receive daily and monthly expense summaries

## Installation

1. Navigate to your Frappe bench directory:
```bash
cd /path/to/frappe-bench
```

2. Clone or link this app:
```bash
bench get-app expense_tracker /path/to/expense_tracker
```

3. Install the app:
```bash
bench install-app expense_tracker
```

4. Build assets:
```bash
bench build
```

5. Restart the bench:
```bash
bench restart
```

## Usage

### Creating Expense Categories

1. Go to Expense Tracker > Expense Category
2. Click "New"
3. Enter:
   - Category Name (e.g., "Food", "Transport")
   - Optional: Monthly Budget Limit
   - Optional: Color for visual identification
4. Save

### Adding Expenses

1. Go to Expense Tracker > Expense
2. Click "New"
3. Fill in the details:
   - Date (defaults to today)
   - Category (select from existing categories)
   - Amount
   - Description
   - Payment Method
   - Vendor/Payee
   - Optional: Attach Receipt Image
4. Save and Submit

### Viewing Reports

1. Go to Expense Tracker > Expense
2. Use the filters to view expenses by date range, category, or status
3. Click the menu (...) to export to CSV

## API Endpoints

### Get Expenses
```
GET /api/method/expense_tracker.api.expense_api.get_expenses
```

### Create Expense
```
POST /api/method/expense_tracker.api.expense_api.create_expense
```

### Get Dashboard Data
```
GET /api/method/expense_tracker.api.expense_api.get_dashboard_data
```

### Export to CSV
```
GET /api/method/expense_tracker.api.expense_api.export_to_csv
```

## DocTypes

### Expense
Main transaction document for recording expenses.

**Fields:**
- Date (required)
- Category (required, Link to Expense Category)
- Amount (required, Currency)
- Description
- Payment Method (Select)
- Vendor/Payee
- Receipt Attached (Check)
- Receipt Image (Attach Image)
- Status (Read Only: Pending/Verified/Approved/Rejected)

### Expense Category
Master data for expense categories.

**Fields:**
- Category Name (required, unique)
- Description
- Monthly Budget Limit (Currency)
- Is Active (Check)
- Color

## Folder Structure

```
expense_tracker/
├── expense_tracker/
│   ├── __init__.py              # App initialization
│   ├── hooks.py                 # Frappe hooks
│   ├── api/                     # API endpoints
│   │   ├── __init__.py
│   │   └── expense_api.py
│   ├── config/                  # Configuration files
│   ├── modules/                 # Application modules
│   │   └── expenses/
│   │       ├── doctype/
│   │       │   ├── expense/     # Expense DocType
│   │       │   └── expense_category/  # Category DocType
│   │       └── __init__.py
│   ├── public/                  # Public assets
│   │   ├── js/
│   │   └── css/
│   ├── templates/               # Jinja templates
│   ├── expense_events.py        # DocType event handlers
│   ├── notifications.py         # Notification configuration
│   └── tasks.py                 # Scheduled tasks
├── package.json
└── README.md
```

## License

MIT
# watchman
