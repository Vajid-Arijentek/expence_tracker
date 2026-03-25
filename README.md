# watchman

Expense Tracker - A simple daily expense tracking application for Frappe Framework.

## Quick Start with Docker

```bash
docker-compose up -d
```

Access the application at: http://localhost:8000

**Default Credentials:**
- Username: `admin`
- Password: `admin`

## Project Structure

```
expense_tracker/
├── apps/
│   └── expense_tracker/       # Main Frappe application
│       ├── __init__.py
│       ├── hooks.py
│       ├── api/
│       ├── modules/
│       ├── public/
│       └── templates/
└── docker-compose.yml         # Docker configuration
```

## Features

- Expense tracking with categories
- Budget management per category
- Receipt attachments
- Status tracking (Pending, Verified, Approved, Rejected)
- Dashboard with daily/monthly/yearly summaries
- CSV export
- Email notifications for daily/monthly summaries

## Manual Installation (Frappe Bench)

```bash
cd /path/to/frappe-bench
bench get-app expense_tracker ./apps/expense_tracker
bench install-app expense_tracker
bench build
bench restart
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/method/expense_tracker.api.expense_api.get_expenses` | GET | Get all expenses |
| `/api/method/expense_tracker.api.expense_api.create_expense` | POST | Create new expense |
| `/api/method/expense_tracker.api.expense_api.get_dashboard_data` | GET | Get dashboard summary |
| `/api/method/expense_tracker.api.expense_api.export_to_csv` | GET | Export to CSV |

## License

MIT
