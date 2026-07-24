# PulseAI — Technical Architecture

*Status: reflects the implementation as of this document's creation. PulseAI is an active WIP POC — see [Known limitations](#known-limitations--current-state) for what's intentionally not built yet.*

## 1. What PulseAI is

PulseAI is a delivery-intelligence platform for Agile software projects. It syncs real delivery data (Jira today, more connectors planned), computes health/risk/effort/confidence signals from that data instead of manual reporting, and exposes it through an executive dashboard and a role-scoped "Ask PulseAI" chat assistant — for both the delivery team (super_admin) and the customer paying for the project (customer role).

## 2. High-level architecture

```mermaid
graph TB
    subgraph Client
        Browser["Browser<br/>(Next.js SPA, JWT in localStorage)"]
    end

    subgraph "Docker Compose stack (single host, port 8080 → 80)"
        Nginx["nginx : 80<br/>reverse proxy"]
        Frontend["frontend : 3000<br/>Next.js 14 (App Router)"]
        API["api : 8000<br/>FastAPI + Uvicorn"]
        Worker["worker<br/>ARQ background jobs"]
        Redis[("Redis 7<br/>ARQ job queue")]
    end

    subgraph "External / managed services"
        Supabase[("Supabase Postgres<br/>(pooler, ap-southeast-1)")]
        SupaStorage[("Supabase Storage<br/>bucket: pulseai-documents")]
        Jira["Jira Cloud REST/Agile API<br/>(pulseaipoc.atlassian.net)"]
        Groq["Groq API<br/>(LLM, multi-key rotation)"]
        Gemini["Gemini API<br/>(LLM fallback, multi-key rotation)"]
    end

    Browser -->|HTTPS :8080| Nginx
    Nginx -->|"/ → :3000"| Frontend
    Nginx -->|"/api/ → :8000"| API
    Frontend -->|"NEXT_PUBLIC_API_URL=/api<br/>(same-origin via nginx)"| Nginx

    API -->|asyncpg| Supabase
    API -->|enqueue jobs| Redis
    API --> SupaStorage
    API --> Jira
    API --> Groq
    API --> Gemini

    Worker -->|asyncpg, own session per job| Supabase
    Worker -->|dequeue jobs / cron| Redis
    Worker --> Jira
    Worker --> Groq
    Worker --> Gemini

    style Browser fill:#1e293b,color:#fff
    style Nginx fill:#334155,color:#fff
    style Frontend fill:#0f766e,color:#fff
    style API fill:#1d4ed8,color:#fff
    style Worker fill:#7c3aed,color:#fff
    style Redis fill:#b91c1c,color:#fff
    style Supabase fill:#065f46,color:#fff
    style SupaStorage fill:#065f46,color:#fff
    style Jira fill:#92400e,color:#fff
    style Groq fill:#374151,color:#fff
    style Gemini fill:#374151,color:#fff
```

**Note on the Postgres/Redis containers**: `docker-compose.yml` defines a local `postgres` and `redis` service (with healthchecks), but `backend/.env` sets `DATABASE_URL` to a remote **Supabase** Postgres pooler connection — the app actually talks to Supabase, not the bundled local Postgres container. Redis *is* actually used locally, for the ARQ queue. This is a real, current inconsistency worth cleaning up (either drop the unused local `postgres` service, or make Supabase-vs-local switchable via env).

## 3. Deployment topology

| Service | Image / build | Listens on | Depends on | Purpose |
|---|---|---|---|---|
| `nginx` | `nginx:1.27-alpine` | host `8080` → container `80` | api (healthy), frontend (started) | Single entrypoint; routes `/api/*` to backend, everything else to frontend. Buffering disabled + 300s read timeout on `/api/` to support SSE streaming (chat/analysis). |
| `frontend` | `./frontend/Dockerfile` (Node 20) | `3000` (internal) | api (healthy) | Next.js 14 App Router SPA. `NEXT_PUBLIC_API_URL=/api` is baked in at **build time** via Docker `ARG`/`ENV` (a past bug: it was previously read at runtime, causing stale API URLs — fixed). |
| `api` | `./backend/Dockerfile` (Python 3.12) | `8000` (internal) | postgres (healthy, unused — see above), redis (healthy) | FastAPI app, `uvicorn app.main:app`. Auto-runs Alembic migrations + seed on boot. Healthcheck hits `/healthz`. |
| `worker` | same image as `api` | — (no HTTP port) | postgres (healthy), redis (healthy) | Runs `arq app.worker.WorkerSettings` — the ARQ job consumer + cron scheduler. Healthcheck disabled (nothing listens on 8000 in this container). |
| `postgres` | `postgres:16-alpine` | `5432` | — | Defined in compose but **not actually used** by the app (see note above); `DATABASE_URL` points to Supabase instead. |
| `redis` | `redis:7-alpine` | `6379` | — | Backs the ARQ job queue; password-protected via `REDIS_PASSWORD`. Actually used. |

`docker-compose.override.yml` remaps nginx to host port `8080` (so the stack can run alongside other services on the same box without conflicting on 80).

## 4. Backend architecture (`backend/app/`)

### 4.1 Layering

```mermaid
graph LR
    R["Routers<br/>(backend/app/routers/*.py)<br/>HTTP contract, auth, scoping"]
    S["Services<br/>(backend/app/services/*.py)<br/>business logic, orchestration"]
    M["Models<br/>(backend/app/models/*.py)<br/>SQLAlchemy ORM"]
    L["LLM client<br/>(backend/app/llm/*.py)"]
    C["Connectors<br/>(backend/app/connectors/*.py)"]
    DB[("Supabase Postgres")]

    R --> S
    S --> M
    S --> L
    S --> C
    M --> DB
```

Routers never touch the DB or call the LLM directly — they resolve the current user, enforce scoping (`_load_project`, `_scope`), and delegate to a service function. Services contain all business logic and are the only layer that talks to models/DB, the LLM client, or connectors. This is a strict, consistently-applied separation across the whole backend.

### 4.2 Routers → endpoints (`backend/app/routers/`)

| Router | Key endpoints |
|---|---|
| `auth.py` | `POST /auth/login`, `GET /auth/me`, `PUT /auth/me/password` |
| `customers.py` | `GET/POST /customers`, `GET/PATCH /customers/{id}` |
| `projects.py` | `GET /customers/{id}/projects`, `GET/PATCH /projects/{id}`, `POST/GET /projects/{id}/outcome`. Also defines the shared `_load_project()` scoping helper used across nearly every other router. |
| `connectors.py` | `GET/POST /projects/{id}/connectors`, `.../test`, `.../sync` (enqueues `run_jira_sync`), `.../status`; `GET /projects/{id}/sprints`, `.../stories` |
| `analysis.py` | `POST/GET /projects/{id}/analysis/{kind}`, `POST/GET .../analysis/{analysis_id}/judge` |
| `documents.py` | `GET/POST /projects/{id}/documents`, `GET/DELETE /documents/{id}`, `GET /projects/{id}/requirements/drift` |
| `confidence.py` | `POST /projects/{id}/confidence/compute`, `GET /projects/{id}/confidence`, `POST /projects/{id}/alignment` |
| `dashboard.py` | `GET /projects/{id}/dashboard`, `GET /projects/{id}/scope-creep` |
| `resources.py` | `GET /projects/{id}/resources` (risk view) + full roster/leave CRUD |
| `dependencies.py` | `GET /projects/{id}/dependencies` |
| `decisions.py` | `GET /projects/{id}/decisions` |
| `prediction.py` | `POST /projects/{id}/prediction/compute`, `GET /projects/{id}/prediction` |
| `sentiment.py` | `GET /projects/{id}/sentiment` |
| `simulation.py` | `POST /projects/{id}/simulate` |
| `portfolio.py` | `GET /portfolio` (super_admin only) |
| `action_items.py` | `GET /projects/{id}/action-items`, `PATCH .../action-items/{id}` |
| `risks.py` | `GET /projects/{id}/risks`, `POST .../risks/scan`, `PATCH .../risks/{id}` |
| `chat_scoped.py` | `POST/GET /chat/sessions`, `GET/POST /chat/sessions/{id}/messages` |

### 4.3 Services (`backend/app/services/`)

| Service | Responsibility |
|---|---|
| `dashboard_service.py` | Assembles the composite dashboard payload (health, effort, confidence, sprint/risk/recommendation summaries) in one call. |
| `effort_service.py` | Effort vs. estimate (consumed hours = completed story points × 6.5 vs. `total_person_hours`) and overshoot-risk banding; writes a rule-based row into the risk registry. |
| `prediction_service.py` | Delivery-date prediction: rule-based velocity projection + LLM judge blend. |
| `confidence_service.py` | Confidence score: `0.6 × rule_score + 0.4 × judge_score`, banded red/amber/green. |
| `scope_service.py` | Scope-creep detection: diffs current scope vs. earliest baseline snapshot. |
| `risk_service.py` | LLM "Risk Identifier" agent — scans documents + live signals, upserts into the persisted risk registry with active/mitigated/closed lifecycle. |
| `resource_service.py` | Resource risk (capacity/burnout/knowledge concentration) + roster/leave CRUD. |
| `knowledge_service.py` | Bus-factor / knowledge-concentration detection from story labels × assignees. |
| `volatility_service.py` | Requirement volatility score from reopens/supersessions/scope growth. |
| `dependency_service.py` | LLM-inferred hidden dependency chains between stories/documents/signals. |
| `decision_service.py` | Customer decision-delay tracking from simulated Teams payloads + transcripts. |
| `requirement_service.py` | Requirement drift: persists extracted requirements so undelivered ones can be flagged. |
| `document_service.py` | Document upload/extraction pipeline (LLM extraction), triggers downstream syncs. |
| `analysis_service.py` | Generic LLM analyses (`AIAnalysis` rows) per `AnalysisKind`; nightly executive briefing entry point. |
| `judge_service.py` | Second-pass LLM critique of an existing analysis ("AI Judge"). |
| `alignment_service.py` | LLM check that sprints/stories trace back to the documented knowledge base. |
| `chat_service.py` | RAG orchestration for scoped chat — builds context, calls LLM, persists messages. |
| `retrieval.py` | Builds bounded SQL-aggregated context for LLM grounding (no vector DB). |
| `sentiment_service.py` | Stakeholder sentiment trend + reasoning over simulated Teams/Slack signals. |
| `portfolio_service.py` | Cross-project rollup for the portfolio view (super_admin). |
| `simulation_service.py` | "What-if" scenario reasoning (LLM-only, no solver). |
| `outcome_service.py` | Records project outcomes (duration, velocity, defect density, on-time) on completion. |
| `metrics_service.py` | Writes to the generic trend table (`metric_snapshots`) after every sync. |
| `action_item_service.py` | Aggregates action items extracted from documents into a trackable table. |
| `simulated_refresh_service.py` | Nightly bounded random-walk nudge to simulated connector data, so it has real trend history. |
| `jira_sync.py` | Connector sync: fetch → normalize → upsert; fans out cheap recompute jobs on success. |

### 4.4 Data model (core tables, simplified)

```mermaid
erDiagram
    Organization ||--o{ Customer : has
    Organization ||--o{ User : has
    Customer ||--o{ User : "customer-role users"
    Customer ||--o{ Project : has
    Project ||--o{ Connector : has
    Project ||--o{ Sprint : has
    Project ||--o{ Story : has
    Sprint ||--o{ Story : contains
    Project ||--o{ Document : has
    Document ||--o| DocumentExtraction : has
    Project ||--o{ RiskItem : has
    Project ||--o{ RequirementItem : has
    Project ||--o{ ActionItem : has
    Project ||--o{ ConfidenceScore : "history"
    Project ||--o{ DeliveryPrediction : "history"
    Project ||--o{ MetricSnapshot : "trend data"
    Project ||--o{ ChatSession : has
    ChatSession ||--o{ ChatMessage : has
    Project ||--o{ ProjectResource : "roster"
    ProjectResource ||--o{ ResourceLeave : has
    Project ||--o| ProjectOutcome : "on completion"

    Project {
        uuid customer_id FK
        string key
        enum status
        enum industry
        float total_person_hours
    }
    Story {
        uuid sprint_id FK
        string external_id
        enum status_category
        float story_points
        bool is_blocked
        uuid carried_forward_from_sprint_id
    }
    RiskItem {
        string title
        enum severity
        enum status
        enum source_type
    }
```

Two append-only "history" tables (`ConfidenceScore`, `DeliveryPrediction`) preserve every computed value over time for trend charts; most other AI-derived tables (`RiskItem`, `RequirementItem`, `KnowledgeMapEntry`) are upserted/recomputed-in-place instead, since they represent current state rather than a time series. `MetricSnapshot` is a generic `(project_id, metric_key, value, recorded_at)` table shared by velocity/scope/effort trend consumers — one schema for every kind of trend rather than a table per metric.

### 4.5 Auth & scoping model

```mermaid
sequenceDiagram
    participant B as Browser
    participant N as nginx
    participant A as FastAPI (auth.py)
    participant R as Any router (e.g. dashboard.py)
    participant DB as Supabase Postgres

    B->>N: POST /api/auth/login {email, password}
    N->>A: POST /auth/login
    A->>DB: look up User, verify password hash
    A-->>B: {token} — JWT, HS256, 8h expiry<br/>payload: sub, role, customer_id, org_id

    Note over B: token stored in localStorage ("pulse_token")

    B->>N: GET /api/projects/{id}/dashboard<br/>Authorization: Bearer <token>
    N->>R: forward request
    R->>A: _get_current_user() dependency — decode + validate JWT
    A->>DB: load User row, check is_active
    R->>R: _load_project(db, project_id, user)
    alt user.role == customer
        R->>DB: load Project, load Customer
        R->>R: 403 if customer.id != user.customer_id
    else user.role == super_admin
        R->>R: no ownership check
    end
    R->>DB: run service logic
    R-->>B: 200 payload (or 403/404)
```

`_load_project()` (defined once in `projects.py`, imported everywhere) is the single enforcement point for project-level access — every project-scoped router uses it, so there is one place to audit for authorization bugs rather than N ad-hoc checks. Chat sessions have a parallel scoping path (`chat_scoped.py::_load_scoped_session`) since a session can be scoped to a project, a customer, or an industry rather than only a project.

## 5. Key data flows

### 5.1 Jira sync → recompute fan-out

```mermaid
sequenceDiagram
    participant U as User (UI)
    participant API as FastAPI
    participant Q as Redis (ARQ queue)
    participant W as Worker
    participant J as Jira Cloud API
    participant DB as Postgres

    U->>API: POST /projects/{id}/connectors/{cid}/sync
    API->>Q: enqueue run_jira_sync(connector_id)
    API-->>U: 202 Accepted

    Q->>W: dequeue run_jira_sync
    W->>DB: connector.status = syncing
    W->>J: fetch statuses, sprints, issues (paginated, retried on 429)
    J-->>W: raw Jira data
    W->>W: normalize into NormalizedBundle
    W->>DB: upsert StatusRef, Sprint, Story (by external_id)
    W->>DB: connector.status = connected, last_synced_at = now
    W->>Q: enqueue append_velocity_snapshot, recompute_effort_risk,<br/>append_scope_snapshot, recompute_knowledge_map,<br/>recompute_confidence, recompute_prediction

    par cheap rule-based jobs (no LLM cost)
        Q->>W: append_velocity_snapshot
        Q->>W: recompute_effort_risk
        Q->>W: append_scope_snapshot
        Q->>W: recompute_knowledge_map
        Q->>W: recompute_confidence
        Q->>W: recompute_prediction
    end
```

The split between "cheap, rule-based, runs after every sync" and "LLM-heavy, nightly-cron-only" jobs is a deliberate cost-control convention followed throughout the codebase — see 5.3.

### 5.2 Dashboard request (composite payload)

```mermaid
flowchart TD
    A["GET /projects/id/dashboard"] --> B["_load_project — auth/scope check"]
    B --> C["dashboard_service.get_dashboard"]
    C --> D["build_context — totals, status_counts"]
    C --> E["prediction_service.latest_prediction<br/>→ schedule_score"]
    C --> F["scope_service.scope_growth_metrics<br/>→ scope_penalty"]
    C --> G["effort_service.compute_effort<br/>→ effort_penalty (overshoot_risk)"]
    D & E & F & G --> H["health = 0.45×completion + 0.20×schedule<br/>+ 0.20×scope + 0.15×effort"]
    C --> I["confidence_service.latest_confidence"]
    C --> J["analysis_service.latest_analysis<br/>(risk / recommendations / executive)"]
    C --> K["sprint/blocked-story queries"]
    H & I & J & K --> L["single JSON payload"]
    L --> M["frontend: HealthGauge, EffortPanel,<br/>ConfidenceMeter, PredictionCard, risk cards"]
```

All of this happens in **one request**, entirely from already-computed/cheap-to-read data — no LLM call sits on this hot path (the LLM analyses/confidence/prediction values were computed asynchronously by the worker and are just read here). This is why the dashboard loads fast despite blending five distinct signals.

### 5.3 Nightly cron fan-out

```mermaid
flowchart LR
    Cron1["cron 02:00<br/>refresh_simulated_signals"] --> Sim["nudge every SimulatedDataset row<br/>+ append metric_snapshots"]
    Cron2["cron 02:15<br/>nightly_all_projects"] --> Fan{"for each project in DB"}
    Fan --> P1["detect_dependencies (LLM)"]
    Fan --> P2["recompute_knowledge_map (rule)"]
    Fan --> P3["generate_executive_briefing (LLM)"]
    Fan --> P4["compute_requirement_volatility (rule)"]
    Fan --> P5["scan_project_risks (LLM, safety net —<br/>primary trigger is document upload)"]
```

### 5.4 Ask PulseAI (scoped chat / RAG)

```mermaid
sequenceDiagram
    participant U as User
    participant API as chat_scoped.py
    participant Ret as retrieval.py
    participant LLM as llm/client.py
    participant DB as Postgres

    U->>API: POST /chat/sessions {project_id? | customer_id? | industry?}
    API->>API: resolve scope by role<br/>(customer → forced to own customer_id;<br/>super_admin → whatever was requested)
    API->>DB: create ChatSession
    API-->>U: session

    U->>API: POST /chat/sessions/{id}/messages {content}
    API->>API: resolve_project_ids(scope) — AND-combines<br/>customer_id + industry filters if both set
    API->>Ret: build_context(db, project_ids)
    Ret->>DB: bounded SQL aggregates (stories, risks, docs) —<br/>no vector DB, context assembled directly from tables
    Ret-->>API: compact context string
    API->>LLM: stream(prompt + context)
    LLM->>API: candidate key/provider loop<br/>(Groq keys → Gemini keys) until one succeeds
    LLM-->>API: text delta stream (SSE)
    API-->>U: streamed answer + citations
    API->>DB: persist ChatMessage (both sides)
```

### 5.5 Risk registry — two writers, one table

```mermaid
flowchart TD
    subgraph "LLM writer (risk_service.py)"
        A1["scan_project_risks<br/>(nightly cron + document-upload trigger)"] --> A2["LLM reads documents + live signals,<br/>fed existing active titles to avoid duplicates"]
    end
    subgraph "Rule-based writer (effort_service.py)"
        B1["recompute_effort_risk<br/>(after every Jira sync)"] --> B2["fixed title 'Effort overshoot risk'<br/>banded low/medium/high from overshoot_pct"]
    end
    A2 --> C[("risk_items table<br/>upsert-by-title, active/mitigated/closed")]
    B2 --> C
    C --> D["GET /projects/id/risks<br/>+ dashboard risk_cards"]
```

Both writers upsert into the same `risk_items` registry using an exact-title match within the currently-active set, so a rule-based row (e.g. "Effort overshoot risk") and an LLM-authored row never collide as long as titles differ — the LLM path is explicitly given existing active titles as context to avoid re-inventing near-duplicates.

## 6. LLM layer (`backend/app/llm/`)

```mermaid
flowchart TD
    Call["service calls llm.client.complete() / .stream()"] --> Cand["_candidates(model):<br/>1. every Groq key for the requested model<br/>2. every Gemini key (fallback model)<br/>3. every remaining key of the other provider"]
    Cand --> Try{"try next (model, key) pair"}
    Try -->|success| Log["log to llm_call_logs<br/>(tokens, cost, duration, status)"] --> Done["return content"]
    Try -->|AuthenticationError| Try
    Try -->|RateLimitError 429| Try
    Try -->|all candidates exhausted| Fail["502 LLM upstream error"]
```

- Multi-provider (**Groq** primary, **Gemini** fallback) via **LiteLLM**, with up to ~4 keys per provider (`GROQ_API_KEYS`/`GEMINI_API_KEYS`, comma-separated) rotated on failure — the design goal is that a single dead/rate-limited key never fails a request while any other configured key could serve it.
- Every call, success or failure, is logged to `llm_call_logs` (feature, model, tokens, cost via `pricing.calculate_cost`, duration, status) — full LLM spend/usage observability per project/feature.
- `stream()` only retries across candidates before the first chunk is yielded; once streaming starts, failures propagate rather than silently retrying (avoids duplicated partial output to the client).
- Per-feature model defaults: analysis/judge use the larger `llama-3.3-70b-versatile`, chat uses the smaller/faster `llama-3.1-8b-instant`.

## 7. Frontend architecture (`frontend/src/`)

### 7.1 Route tree

```
app/
├── layout.tsx              root layout, <QueryProvider>
├── page.tsx                "/" → redirect("/login")
├── login/                  "/login"
└── (app)/                  authenticated shell (AppShell: sidebar + topbar + chat FAB)
    ├── portfolio/           "/portfolio" — cross-customer rollup (super_admin)
    ├── customers/           "/customers", "/customers/[id]"
    ├── projects/            "/projects" → redirect("/customers"); "/projects/[id]/*"
    │   └── [id]/
    │       ├── (overview)   executive dashboard
    │       ├── analysis/    "Project intelligence"
    │       ├── chat/        "Ask PulseAI" (project-scoped)
    │       ├── documents/
    │       ├── resources/
    │       ├── risks/
    │       ├── sentiment/
    │       └── settings/    connectors, project outcome
    └── chat/                "/chat" — global, role-aware scope picker
```

Every route follows a consistent **page.tsx (server, thin) → `*-content.tsx` (client, data-fetching)** split.

### 7.2 Data flow: API client → hooks → components

```mermaid
flowchart LR
    Comp["*-content.tsx components"] --> Hook["React Query hooks<br/>(frontend/src/hooks/*.ts)"]
    Hook --> ApiTs["api.ts — single client,<br/>namespaced by domain (api.dashboard, api.risks, ...)"]
    ApiTs -->|"fetch + Bearer token<br/>+ centralized 401 handling"| Nginx["nginx /api/*"]
    Chat["chat components"] -->|"streamSSE()"| Stream["stream.ts — hand-rolled SSE reader"]
    Stream --> Nginx
    Types["types/api.ts — DTOs mirroring<br/>backend Pydantic schemas"] -.-> ApiTs
    Types -.-> Hook
```

- One `api` object in `lib/api.ts`, one function per REST endpoint, all typed against the single `types/api.ts` contract file.
- JWT lives in `localStorage` only (`pulse_token`) — no cookies, no Next.js middleware; `AppShell` client-side-redirects to `/login` if the token is missing, and any `401` response clears the token and hard-redirects.
- Role (`super_admin` vs `customer`) is decoded directly from the JWT payload client-side (`lib/auth.ts`), not fetched from `/auth/me` — drives sidebar nav, chat scope picker, and post-login landing route (`customer` with 1 project → straight into it; with multiple → their customer detail page; `super_admin` → portfolio-first).

## 8. Known limitations / current state

- Local `postgres`/`redis` services in compose vs. actual Supabase DB connection — worth reconciling (see §2 note).
- Only **Jira** is a real connector; Teams/Slack/ClickUp/Asana/Trello/resource/budget/timeline/sentiment connector types exist in the schema but fall back to simulated data regardless of configured mode.
- No automated test suite / CI gate yet — this repo's changes have been verified by direct testing against the live deployed stack.
- No SSO/enterprise auth, no self-serve tenant onboarding — projects/customers are currently created by a super_admin.
- Auth is fully client-side (JWT decoded in the browser, no server-side session) — acceptable for a POC, would need hardening (short-lived tokens + refresh, or server-verified session) before wider external exposure.

## 9. Where to look for more detail

- `setup.md` — how to stand up the stack from scratch on Ubuntu.
- `backend/migrations/versions/` — schema evolution, migration-by-migration.
- `project/` — BRDs (per-project requirements source documents) and sample call transcripts used to validate scope-creep/requirement-drift detection.
- `docs/ai-features-gap-analysis-and-plan.md` — the original feature-by-feature gap analysis this build was driven from.
