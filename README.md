# Upkeep — CMMS

A **Computerized Maintenance Management System** with a Python/FastAPI backend and a React frontend.  
Academic project — see [TEAM.md](TEAM.md) for module ownership and the team workflow.

---

## Tech Stack

### Backend

| Layer | Technology |
|-------|-----------|
| Runtime | Python 3.11+ |
| Web framework | FastAPI |
| Async DB driver | Motor (MongoDB) |
| Validation | Pydantic v2 |
| Testing | pytest + pytest-asyncio |
| Local DB | Docker / MongoDB 7 |

### Frontend

| Layer | Technology |
|-------|-----------|
| Bundler | Vite 5 |
| UI | React 18 (JSX) |
| Routing | React Router v6 |
| HTTP | axios |
| Styling | Tailwind CSS v3 |

---

## Getting Started

### Prerequisites

- Python 3.9+ (3.11+ recommended)
- Node.js 18+ and npm
- Docker + Docker Compose

### 1 — Clone & create virtual environment

```bash
git clone <repo-url>
cd upkeep
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2 — Start MongoDB

```bash
docker-compose up -d
```

### 3 — Configure environment

```bash
cp .env.example .env
# Edit .env if you need a non-default Mongo URI
```

### 4 — Run the server

```bash
uvicorn app.main:app --reload
```

- API root: http://localhost:8000  
- Interactive docs (Swagger UI): http://localhost:8000/docs  
- Alternative docs (ReDoc): http://localhost:8000/redoc  
- Health check: http://localhost:8000/health

### 5 — Run tests

```bash
pytest
# with coverage:
pytest --cov=app --cov-report=term-missing
```

### 6 — Run the frontend

In a **second terminal**:

```bash
cd frontend
cp .env.example .env   # defaults to http://localhost:8000/api — usually no edit needed
npm install
npm run dev
```

The React app starts at **http://localhost:5173** and talks to the FastAPI server at **:8000**.

> **CORS note:** `app/main.py` includes `CORSMiddleware` configured to allow
> `http://localhost:5173`. If you change the Vite port, update the `allow_origins`
> list in `main.py` to match.

---

## Project Structure

```
upkeep/
├── app/
│   ├── main.py                    # FastAPI app, lifespan, router registration
│   ├── core/
│   │   ├── config.py              # pydantic-settings — reads .env
│   │   └── database.py            # motor client, get_db() dependency
│   ├── models/                    # Domain entities (pure Python, no DB logic)
│   │   ├── base.py                # BaseEntity: id, timestamps, to/from_mongo
│   │   ├── user.py                # User + Role enum
│   │   ├── work_order.py          # WorkOrder + WorkOrderStatus enum
│   │   ├── asset.py               # Asset + AssetStatus enum
│   │   ├── maintenance.py         # MaintenanceSchedule + TriggerType enum
│   │   └── inventory.py           # InventoryItem
│   ├── schemas/                   # Pydantic DTOs (Create / Update / Response)
│   ├── repositories/
│   │   ├── base_repository.py     # Generic async CRUD (Repository pattern)
│   │   └── *_repository.py        # One per entity, inherits BaseRepository
│   ├── services/                  # Business logic — one class per domain
│   └── api/routes/                # FastAPI routers — one per entity
└── tests/
    ├── conftest.py                # Shared fixtures (ASGI test client)
    └── test_*.py                  # One test file per module
```

### Design Principles

- **DB access only in repositories.** Services and routes never import motor.
- **One service per domain.** Cross-domain calls go through the service API, never directly to another domain's repository.
- **Pydantic v2 for validation.** All external input validated at the route layer before reaching services.
- **Async throughout.** All DB calls use `await`; pytest-asyncio runs tests async.

---

## API Endpoints (skeleton)

| Method | Path | Owner | Description |
|--------|------|-------|-------------|
| GET | `/health` | M1 | Mongo ping health check |
| POST/GET/PATCH/DELETE | `/api/v1/work-orders` | M1 | Work order CRUD |
| POST | `/api/v1/work-orders/{id}/transition` | M1 | Status lifecycle transition |
| POST/GET/PATCH/DELETE | `/api/v1/assets` | M2 | Asset CRUD |
| POST/GET/PATCH/DELETE | `/api/v1/maintenance` | M3 | Maintenance schedule CRUD |
| POST | `/api/v1/maintenance/evaluate` | M3 | Trigger due-schedule evaluation |
| POST/GET/PATCH/DELETE | `/api/v1/inventory` | M4 | Inventory CRUD |
| GET | `/api/v1/inventory/low-stock` | M4 | Items below threshold |
| POST | `/api/v1/inventory/{id}/consume` | M4 | Deduct stock |
| POST | `/api/v1/inventory/{id}/restock` | M4 | Add stock |
| POST/GET/PATCH/DELETE | `/api/v1/users` | M1 | User management |

All unimplemented endpoints return `501 Not Implemented` until the owning member fills them in.

---

## Team

See [TEAM.md](TEAM.md) for the full task split, OOP pattern assignments, integration points, and Git workflow.
