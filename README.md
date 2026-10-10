# Village Finance Management API

FastAPI + PostgreSQL backend for the React village finance application.

## 1. Requirements
- Python 3.10+
- PostgreSQL running locally
- Create an empty database named `village_finance`

In pgAdmin, create a database: **village_finance**. The database user must have permission to create tables.

## 2. Install and configure (Windows PowerShell)

```powershell
cd village_finance_api
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set your PostgreSQL password. Example:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/village_finance
FRONTEND_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

If your password contains characters such as `@`, `:`, `/`, or `#`, URL-encode them.

## 3. Run the API

```powershell
uvicorn app.main:app --reload
```

Open:
- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

Tables are created automatically on first startup. For production, use Alembic migrations instead of `create_all`.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/dashboard/summary` | Dashboard totals |
| POST | `/api/members` | Register a member |
| GET | `/api/members` | List/search members (`?search=name`) |
| GET | `/api/members/{member_id}` | Get one member |
| PATCH | `/api/members/{member_id}` | Update a member |
| DELETE | `/api/members/{member_id}` | Delete member only if no financial records |
| POST | `/api/fund/transactions` | Add deposit or repayment |
| GET | `/api/fund/transactions` | List fund transactions |
| POST | `/api/loans` | Create loan and calculate interest |
| GET | `/api/loans` | List loans |
| PATCH | `/api/loans/{loan_id}/status?status=closed` | Update loan status |
| POST | `/api/expenses` | Record an expense |
| GET | `/api/expenses` | List expenses |
| DELETE | `/api/expenses/{expense_id}` | Delete expense |

## Loan interest rules

`interest_method` can be:
- `simple`: annual rate, prorated by months. Formula: `interest = principal * (annual_rate / 100) * (months / 12)`.
- `flat_monthly`: rate is interpreted as a monthly percentage. Formula: `interest = principal * (rate / 100) * months`.

Example loan payload:

```json
{
  "member_id": 1,
  "principal": 20000,
  "annual_interest_rate": 12,
  "duration_months": 12,
  "interest_method": "simple",
  "loan_date": "2026-10-10",
  "note": "Community fund loan"
}
```

Returns the computed `interest_amount`, `total_amount`, and `monthly_installment`.

## React connection

Use `http://127.0.0.1:8000` as the API base URL. Example:

```js
const response = await fetch("http://127.0.0.1:8000/api/members");
const members = await response.json();
```

Use `http://127.0.0.1:8000/docs` to test endpoints interactively.

## Important notes
- This starter stores monetary values as floating-point columns for simplicity. For real financial records, switch to `NUMERIC(12, 2)` / Python `Decimal` before production.
- This is a starter backend, not yet an accounting-grade ledger: fund balance reconciliation, repayment allocation between principal/interest, authentication, authorization, audit logs, backups, and Alembic migrations should be added before live use.
- `flat_monthly` is a flat-rate calculation, not reducing-balance interest. Confirm the community's agreed interest policy before using real loans.
