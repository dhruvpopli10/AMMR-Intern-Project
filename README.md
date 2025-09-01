# Wallet Service (FastAPI)

A minimal wallet system built with **FastAPI** and **SQLite**.

## Features
- **List Users API** – Fetch all users (name, email, phone) + wallet balance.
- **Update Wallet API** – Add/subtract amount (`mode=delta`) or set absolute balance (`mode=set`). Each action creates a transaction.
- **Fetch Transactions API** – List all wallet transactions for a user.
- Bonus: **Create User API** to add seed users quickly.

## Quick Start

### 1) With Python
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open **http://127.0.0.1:8000/docs** for Swagger.

### 2) With Docker
```bash
docker build -t wallet-api .
docker run -p 8000:8000 --name wallet wallet-api
```

## API Endpoints
- `GET /users` – list users
- `POST /users` – create user
- `POST /users/{user_id}/wallet/adjust` – body:
```json
{
  "mode": "delta",
  "amount": 250.0,
  "description": "Top-up via UPI"
}
```
- `GET /users/{user_id}/transactions` – list transactions

## Notes
- SQLite DB stored at `app.db` in project root.
- Transactions record `credit`, `debit`, or `adjust` (when setting an absolute balance).

## Example (cURL)
```bash
# Create two users
curl -X POST http://127.0.0.1:8000/users -H "Content-Type: application/json" -d '{"name":"Asha", "email":"asha@example.com","phone":"+91-9000000001"}'
curl -X POST http://127.0.0.1:8000/users -H "Content-Type: application/json" -d '{"name":"Ravi", "email":"ravi@example.com","phone":"+91-9000000002"}'

# Credit 500 to user 1
curl -X POST http://127.0.0.1:8000/users/1/wallet/adjust -H "Content-Type: application/json" -d '{"mode":"delta","amount":500,"description":"UPI top-up"}'

# Set user 1 balance to 1200 (adjust)
curl -X POST http://127.0.0.1:8000/users/1/wallet/adjust -H "Content-Type: application/json" -d '{"mode":"set","amount":1200,"description":"Manual correction"}'

# Fetch users and transactions
curl http://127.0.0.1:8000/users
curl http://127.0.0.1:8000/users/1/transactions
```

## Project Layout
```
.
├── app
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── app.db            # created at runtime
├── Dockerfile
├── README.md
└── requirements.txt
```

---

**Swagger UI:** `/docs`  
**ReDoc:** `/redoc`
