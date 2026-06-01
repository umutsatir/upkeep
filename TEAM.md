# Upkeep CMMS — Team Task Split

Upkeep is a Computerized Maintenance Management System built as a 4-person academic project.
The backend is a Python/FastAPI REST API backed by MongoDB; the frontend is a React SPA.
Each member owns one vertical slice end-to-end: backend model → repository → service → API route → React pages → tests → docs.

---

## Summary

| Member | Module | Backend OOP Pattern | Files |
|--------|--------|--------------------|----|
| [MEMBER-1] `@___` | Core & Work Orders | **State** — status lifecycle transitions | ~18 backend · ~12 frontend |
| [MEMBER-2] `@___` | Asset Tracking | **Repository** — clean persistence boundary | ~6 backend · ~3 frontend |
| [MEMBER-3] `@___` | Preventive Maintenance | **Strategy** — time-based vs usage-based triggers | ~6 backend · ~3 frontend |
| [MEMBER-4] `@___` | Inventory Management | **Decorator** — low-stock alert channels | ~6 backend · ~3 frontend |

> **Important:** MEMBER-1's branch (`feature/core-and-auth`) must be merged into `main` before any other branch is created, because the shared base classes and frontend shell that all other members build on top of live there.

---

## MEMBER-1 — Core & Work Orders

**GitHub:** `@___` · **Branch:** `feature/core-and-auth`

### Backend

**Pattern: State** — implement a `WorkOrderState` abstract base class with a concrete class for each `WorkOrderStatus` value (`OpenState`, `AssignedState`, `InProgressState`, `CompletedState`, `ClosedState`, `CancelledState`). Each state class validates which transitions are legal and raises `InvalidTransitionError` for illegal ones.

| File | Role |
|------|------|
| `app/main.py` | FastAPI app factory, lifespan, CORS, router registration |
| `app/core/config.py` | Pydantic-settings config, reads `.env` |
| `app/core/database.py` | Motor client, `get_db()` FastAPI dependency |
| `app/models/base.py` | `BaseEntity` (id, timestamps, `to_mongo`, `from_mongo`) — **shared by all members** |
| `app/models/user.py` | `User` domain entity + `Role` enum |
| `app/models/work_order.py` | `WorkOrder` + `WorkOrderStatus` + `WorkOrderPriority` enums |
| `app/schemas/user.py` | `UserCreate`, `UserUpdate`, `UserResponse` DTOs |
| `app/schemas/work_order.py` | `WorkOrderCreate`, `WorkOrderUpdate`, `WorkOrderStatusTransition`, `WorkOrderResponse` DTOs |
| `app/repositories/base_repository.py` | Generic `BaseRepository[T]` with async create/get/list/update/delete — **shared by all members** |
| `app/repositories/user_repository.py` | `UserRepository` — `get_by_email` |
| `app/repositories/work_order_repository.py` | `WorkOrderRepository` — `list_by_asset`, `list_by_status`, `list_by_assignee` |
| `app/services/user_service.py` | Auth logic: password hashing, JWT generation, RBAC |
| `app/services/work_order_service.py` | Work order lifecycle; delegates to State objects; calls `InventoryService.consume()` on completion (M4 integration) |
| `app/api/routes/users.py` | CRUD + auth endpoints |
| `app/api/routes/work_orders.py` | CRUD + `POST /{id}/transition` status-change endpoint |

### Frontend

| File | Role |
|------|------|
| `frontend/src/main.jsx` | React entry point |
| `frontend/src/App.jsx` | `BrowserRouter` + all `<Route>` declarations |
| `frontend/src/components/Layout.jsx` | Dark-blue sidebar, nav links, top bar, `<Outlet>` |
| `frontend/src/components/Table.jsx` | Reusable data table — loading / error / empty states |
| `frontend/src/components/StatusBadge.jsx` | Colour-coded pill for status/priority values |
| `frontend/src/components/PageHeader.jsx` | Title + subtitle + action-button slot |
| `frontend/src/api/client.js` | Configured axios instance reading `VITE_API_URL`; error interceptor |
| `frontend/src/api/workOrders.js` | `getAll`, `getById`, `create`, `update`, `transition`, `remove` |
| `frontend/src/pages/Dashboard.jsx` | Overview stat cards + quick-action links |
| `frontend/src/pages/auth/Login.jsx` | Login form |
| `frontend/src/pages/auth/Register.jsx` | Registration form |
| `frontend/src/pages/workOrders/WorkOrderList.jsx` | **Reference implementation** — copy this pattern for other modules |
| `frontend/src/pages/workOrders/WorkOrderDetail.jsx` | Single work order view + status-transition buttons |
| `frontend/src/pages/workOrders/WorkOrderForm.jsx` | Create / edit form |

### Tests

| File | What to cover |
|------|--------------|
| `tests/conftest.py` | Shared ASGI test client fixture |
| `tests/test_health.py` | `/health` endpoint, Mongo ping |
| `tests/test_base_entity.py` | `BaseEntity` id generation, timestamps, `to_mongo`/`from_mongo` round-trip |
| `tests/test_work_orders.py` | WorkOrder CRUD; each valid state transition; `InvalidTransitionError` for illegal transitions; completion deducts inventory (mock `InventoryService`) |

### Docs

- **SRS:** functional requirements for work-order lifecycle, user roles, authentication rules.
- **SDD:** class diagram for the State pattern (`WorkOrderState` hierarchy); sequence diagram for `POST /transition`.
- **README section:** work-orders API endpoints, JWT auth flow.

---

## MEMBER-2 — Asset Tracking

**GitHub:** `@___` · **Branch:** `feature/asset-tracking`

> Depends on MEMBER-1's branch being merged first (needs `BaseEntity`, `BaseRepository`).

### Backend

**Pattern: Repository** — `AssetRepository` is the only layer that touches MongoDB for asset data. The service layer never constructs raw queries; all persistence goes through the repository interface.

| File | Role |
|------|------|
| `app/models/asset.py` | `Asset` domain entity + `AssetStatus` enum; embed a `RepairRecord` value object for repair history |
| `app/schemas/asset.py` | `AssetCreate`, `AssetUpdate`, `AssetResponse` DTOs |
| `app/repositories/asset_repository.py` | `AssetRepository` — `get_by_tag`, `list_by_status`, `list_expiring_warranties` |
| `app/services/asset_service.py` | Asset lifecycle (`activate`, `decommission`, `send_to_maintenance`); `add_repair_record`; warranty expiry alerts; validates `asset_tag` uniqueness |
| `app/api/routes/assets.py` | CRUD endpoints |

### Frontend

| File | Role |
|------|------|
| `frontend/src/api/assets.js` | `getAll`, `getById`, `create`, `update`, `remove` |
| `frontend/src/pages/assets/AssetList.jsx` | Asset list table — status badge, warranty highlight, follow `WorkOrderList` pattern |
| `frontend/src/pages/assets/AssetDetail.jsx` | Asset fields, repair history list, warranty status |
| `frontend/src/pages/assets/AssetForm.jsx` | Create / edit form with all asset fields |

### Tests

| File | What to cover |
|------|--------------|
| `tests/test_assets.py` | Asset CRUD; duplicate `asset_tag` rejection; lifecycle transitions; `add_repair_record` appends correctly; `list_expiring_warranties` returns correct set |

### Docs

- **SRS:** functional requirements for asset tracking, warranty management, repair history.
- **SDD:** class diagram showing `Asset` → `AssetRepository` → `AssetService` layering; `RepairRecord` as an embedded value object.
- **README section:** assets API endpoints, asset lifecycle states.

---

## MEMBER-3 — Preventive Maintenance

**GitHub:** `@___` · **Branch:** `feature/preventive-maintenance`

> Depends on MEMBER-1's branch being merged first. Integrates with MEMBER-1 (calls `WorkOrderService.create()` to auto-generate work orders).

### Backend

**Pattern: Strategy** — define an abstract `MaintenanceTriggerStrategy` base class with a single method `is_due(schedule) -> bool`. Implement two concrete strategies: `TimeBasedStrategy` (compares `last_triggered_at + interval_days` to today) and `UsageBasedStrategy` (compares asset operating hours to `usage_threshold_hours`). `MaintenanceService` selects the right strategy at runtime based on `schedule.trigger_type`.

| File | Role |
|------|------|
| `app/models/maintenance.py` | `MaintenanceSchedule` entity + `TriggerType` enum |
| `app/schemas/maintenance.py` | `MaintenanceScheduleCreate`, `MaintenanceScheduleUpdate`, `MaintenanceScheduleResponse` DTOs |
| `app/repositories/maintenance_repository.py` | `MaintenanceRepository` — `list_active`, `list_by_asset`, `list_due` |
| `app/services/maintenance_service.py` | `evaluate_due_schedules()` selects strategy, calls `WorkOrderService.create()` for each due schedule, updates `last_triggered_at` and recalculates `next_due_at` |
| `app/api/routes/maintenance.py` | CRUD endpoints + `POST /evaluate` to trigger evaluation |

### Frontend

| File | Role |
|------|------|
| `frontend/src/api/maintenance.js` | `getAll`, `getById`, `create`, `update`, `remove`, `evaluateDue` |
| `frontend/src/pages/maintenance/MaintenanceList.jsx` | Schedule list — trigger type, active/inactive, next due date; "Evaluate Due" button |
| `frontend/src/pages/maintenance/MaintenanceDetail.jsx` | Schedule fields, last triggered / next due, link to asset |
| `frontend/src/pages/maintenance/MaintenanceForm.jsx` | Create / edit; conditional fields based on `trigger_type` (time vs usage) |

### Tests

| File | What to cover |
|------|--------------|
| `tests/test_maintenance.py` | Schedule CRUD; `TimeBasedStrategy.is_due()` with past/future dates; `UsageBasedStrategy.is_due()` with various hour counts; `evaluate_due_schedules()` calls `WorkOrderService.create()` the correct number of times (mock service); `next_due_at` recalculated after trigger |

### Docs

- **SRS:** functional requirements for PM scheduling, trigger types, auto-WO generation rules.
- **SDD:** Strategy pattern class diagram (`MaintenanceTriggerStrategy` → `TimeBasedStrategy`, `UsageBasedStrategy`); sequence diagram for `evaluate_due_schedules()` → `WorkOrderService.create()`.
- **README section:** maintenance API endpoints, how to trigger evaluation.

---

## MEMBER-4 — Inventory Management

**GitHub:** `@___` · **Branch:** `feature/inventory`

> Depends on MEMBER-1's branch being merged first. Integrates with MEMBER-1 (parts consumed when a WorkOrder is completed).

### Backend

**Pattern: Decorator** — define a `LowStockNotifier` base class with a `notify(item)` method. Wrap it with `EmailAlertDecorator` and `SlackAlertDecorator`, each adding a delivery channel without modifying the core logic. `InventoryService.consume()` calls the composed notifier when stock drops at or below `low_stock_threshold`.

| File | Role |
|------|------|
| `app/models/inventory.py` | `InventoryItem` entity; embed a `ConsumptionRecord` value object in `consumption_log` |
| `app/schemas/inventory.py` | `InventoryItemCreate`, `InventoryItemUpdate`, `StockAdjustment`, `InventoryItemResponse` DTOs |
| `app/repositories/inventory_repository.py` | `InventoryRepository` — `get_by_sku`, `list_low_stock` |
| `app/services/inventory_service.py` | `consume(item_id, adjustment)` deducts stock, logs against a WO, fires notifier if threshold crossed; `restock(item_id, adjustment)` adds stock; `list_low_stock()` |
| `app/api/routes/inventory.py` | CRUD + `GET /low-stock` + `POST /{id}/consume` + `POST /{id}/restock` |

### Frontend

| File | Role |
|------|------|
| `frontend/src/api/inventory.js` | `getAll`, `getById`, `create`, `update`, `remove`, `getLowStock`, `consume`, `restock` |
| `frontend/src/pages/inventory/InventoryList.jsx` | Item list — highlight low-stock rows in red; "Low Stock Only" toggle |
| `frontend/src/pages/inventory/InventoryDetail.jsx` | Item fields, current stock, consumption log, Consume / Restock action buttons |
| `frontend/src/pages/inventory/InventoryForm.jsx` | Create / edit form |

### Tests

| File | What to cover |
|------|--------------|
| `tests/test_inventory.py` | Item CRUD; `consume()` reduces `quantity_on_hand` and appends to `consumption_log`; `consume()` at/below threshold triggers notifier (mock notifier); `restock()` increases stock; `list_low_stock()` returns correct items |

### Docs

- **SRS:** functional requirements for stock management, low-stock alerting, parts-consumed-per-WO tracking.
- **SDD:** Decorator pattern class diagram (`LowStockNotifier` → `EmailAlertDecorator` → `SlackAlertDecorator`); sequence diagram for `consume()` → notifier chain.
- **README section:** inventory API endpoints, low-stock alert configuration.

---

## Integration Points

These are the cross-module call boundaries. Always program to the **service interface** — never import another module's repository directly. Inject foreign services via FastAPI `Depends()`.

| Boundary | Members | Trigger | Contract |
|----------|---------|---------|----------|
| WorkOrder → Asset | M1 calls M2 | On `WorkOrderService.create()` | Call `AssetService.get(asset_id)`; raise `404` if the asset does not exist |
| WorkOrder → Asset | M1 calls M2 | On `WorkOrderService.transition()` → `COMPLETED` | Call `AssetService.add_repair_record(asset_id, record)` to log the repair |
| WorkOrder → Inventory | M1 calls M4 | On `WorkOrderService.transition()` → `COMPLETED` | Call `InventoryService.consume(item_id, qty, wo_id)` for each entry in `work_order.parts_used` |
| Maintenance → WorkOrder | M3 calls M1 | `MaintenanceService.evaluate_due_schedules()` | Call `WorkOrderService.create(payload)` using the schedule's template fields (`asset_id`, `title`, `description`, `priority`, `assigned_to`) |

**Frontend integration points** (no direct API cross-calls needed; use separate `useEffect` fetches):

- Work order form: `asset_id` field is a searchable select that calls `getAll()` from `api/assets.js` (M2).
- Inventory detail: Consume action links to a work order via a select that calls `getAll()` from `api/workOrders.js` (M1).
- Maintenance form: `asset_id` field calls `getAll()` from `api/assets.js` (M2).

---

## Workflow

```
main
 └── feature/core-and-auth          ← MEMBER-1  ← merge FIRST
 └── feature/asset-tracking         ← MEMBER-2
 └── feature/preventive-maintenance ← MEMBER-3
 └── feature/inventory              ← MEMBER-4
```

1. **MEMBER-1 merges first.** `BaseEntity`, `BaseRepository`, `app/core/*`, and the React Layout + shared components all live in their branch. No other branch should be created until this PR is merged.
2. After M1's merge, each member **branches off `main`** (not off each other's branches).
3. Open a **Pull Request** into `main`; at least one other member must review before merging.
4. Use **`feature/<domain-name>`** branch naming exactly as shown above.
5. No direct pushes to `main`.
6. All `pytest` checks must be green before a PR can be merged.
7. If you need a cross-module type (e.g., `WorkOrderCreate`) that hasn't merged yet, use a minimal stub and leave a `# TODO: remove stub after M1 merges` comment.

### Daily dev setup

```bash
# Terminal 1 — backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
docker-compose up -d          # MongoDB on :27017
cp .env.example .env
uvicorn app.main:app --reload # API on :8000

# Terminal 2 — frontend
cd frontend
cp .env.example .env          # VITE_API_URL=http://localhost:8000/api
npm install
npm run dev                   # React on :5173

# Run tests
pytest
```

- API docs (Swagger UI): http://localhost:8000/docs
- React app: http://localhost:5173
