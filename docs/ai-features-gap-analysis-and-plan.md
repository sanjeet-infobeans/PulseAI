# PulseAI — Gap Analysis & Implementation Plan: 15 AI Delivery-Intelligence Features

## Context

PulseAI today (per `feat: PulseAI POC` + 3 fix-up commits) is a working POC: real Jira sync, a document-upload + LLM-extraction engine, a rule+LLM-judge confidence score, and an LLM-based requirements-alignment engine. Four frontend pages (`/portfolio`, `/executive`, `/resources`, `/sentiment`) already exist as `<ComingSoon future />` placeholders under a "Roadmap" nav group, and a `SimulatedDataset` table already carries plausible-looking JSON for Teams/Slack/resource/budget/timeline/sentiment "connectors" — but that data is seeded once and never updates, and nothing reads its values today (only its key presence, in `dashboard_service.py`).

The user supplied 15 proposed AI features (delivery prediction, scope creep, requirement drift, hidden dependencies, volatility score, decision delay, resource risk, confidence breakdown, executive briefing, AI judge, delivery DNA, knowledge gaps, sentiment, what-if simulation, portfolio intelligence) and asked for a solution-architect-level gap analysis and implementation plan. Decisions already made with the user:
1. Plan **all 15** as a phased roadmap (not just the 5-star items).
2. Keep Teams/Slack/email as **simulated** data sources — design AI logic against the existing `SimulatedDataset` JSONB shape; real OAuth/webhook ingestion is called out once as an explicit **out-of-scope** follow-on, not designed here.
3. Introduce **foundational infra now**: a real job queue + history/time-series tables, because most features need trend-over-time data that doesn't exist today (`confidence_service.py`'s `scope_health` signal is hardcoded to `1.0` with a comment: *"placeholder for scope-churn once history is tracked"* — this plan is what unblocks it).

Goal of this plan: give engineering a concrete, phased build order that maximizes reuse of the existing rule+LLM-judge pattern (`confidence_service.py`), the existing alignment engine (`alignment_service.py`), and the existing bounded-context builder (`retrieval.py`), rather than inventing parallel machinery per feature.

---

## Foundational Infrastructure (build first — unblocks nearly everything below)

### Job queue: ARQ (not Celery)
Redis is already provisioned (`backend/app/redis.py`, `docker-compose.yml`) and every touched service is `async def`/asyncpg (`confidence_service.py`, `retrieval.py`, `document_service.py`, `jira_sync.py`). ARQ runs natively async on the existing Redis client with no new broker; Celery would force a sync/async bridge that doesn't exist anywhere in this codebase today. ARQ's `cron_jobs` also directly covers the "nightly recompute" need without standing up Celery Beat separately.
- New: `backend/app/worker.py` (`WorkerSettings`, one function per job + `cron_jobs=[...]`).
- Replace `BackgroundTasks.add_task(run_sync, ...)` in the connectors router and `process_document`'s background task with `arq_pool.enqueue_job(...)` — this is the literal resolution of `jira_sync.py`'s own "Celery/ARQ is the production path" comment.

### History / time-series tables (new Alembic migration `003_history_infra.py`, following the pattern in `002_widen_doc_type.py`)

One generic append-only snapshot table for anything that's fundamentally a trend, plus a handful of purpose-built tables where the shape needs real columns/joins:

- **`metric_snapshots`** — `project_id`, `sprint_id` (nullable), `metric_key` (e.g. `velocity_completed_points`, `scope_story_count_open`, `sentiment_score`, `resource_utilization_pct`, `budget_forecast_variance_pct`, `timeline_slip_days`, `requirement_volatility_score`, `knowledge_concentration_pct`, `decision_avg_delay_days`), `value` Float, `meta` JSONB, `source`, `recorded_at`. Feeds prediction, scope creep, volatility, resource, sentiment — and finally gives `dashboard_service.py`'s `signals_available` real trendable values instead of just key presence.
- **`requirement_items`** — persists what `retrieval.py::_doc_requirements()` today only computes ad-hoc per call: `text`, `status` (`proposed|covered|missing|superseded|out_of_scope`), `matched_story_keys` JSONB, `source_document_id`, `first_seen_at`/`last_seen_at`/`superseded_by_id`. This is the shared substrate for scope creep, requirement drift, and volatility — build once, don't triplicate.
- **Document versioning** — extend `Document` (`backend/app/models/document.py`) with `version_group_id`, `version`, `supersedes_document_id`; extend `DocumentExtraction` with `diff_from_previous` JSONB. This is what lets drift detection notice "BRD said SSO, a later transcript adds MFA."
- **`dependency_edges`** — `from_type/from_ref`, `to_type/to_ref`, `relation` (`blocks|depends_on|mentioned_in|derived_from|impacts`), `confidence`, `rationale`, `source`.
- **`decision_log`** — `topic`, `requested_at`/`decided_at`, `requested_by`/`decided_by`, `sprint_impact_days`, `status`.
- **`knowledge_map`** — `module_key` (derived from `Story.labels`, which already exists), `developer`, `story_count`, `is_sole_holder`, `computed_at`.
- **`ai_judge_reviews`** — `analysis_id` FK → `ai_analyses`, `coverage_pct`, `missing_risks_count`, `missing_stories_count`, `confidence_pct`, `notes`.
- **`delivery_predictions`** — `sprint_id`, `predicted_completion_date`, `baseline_target_date`, `probability_on_time`, `confidence_pct`, `reasons` JSONB, `recommendations` JSONB.
- **`what_if_scenarios`** — log table: `scenario_text`, `scenario_input`, `estimated_weeks`, `estimated_cost_usd`, `resources_needed`, `risk_delta`, `confidence_delta`, `result_summary`.
- **`ConfidenceScore.sub_scores`** — one new JSONB column on the existing (already time-series) `confidence_scores` table.
- **`Story.reopened_count`** — increment in `jira_sync.py` whenever a re-sync flips a story from `done` back to non-done. Needed for volatility; no way to detect this today.
- **`project_outcomes`** (stub only, Phase 3) — `actual_duration_days`, `actual_velocity_avg`, `defect_density`, `delivered_on_time`, `closed_at`. Create now so it starts accumulating the moment a project completes; do not build logic against it yet (see Phase 3).

### Recompute scheduling
- **On Jira sync** (`jira_sync.py::run_sync`): enqueue cheap/rule-based jobs every time — `recompute_confidence`, `append_velocity_snapshot`, `append_scope_snapshot`, `recompute_knowledge_map`.
- **On document upload complete** (`document_service.py::process_document`): enqueue `sync_requirement_catalog`, and if versioned, `diff_document_version` → `recompute_alignment` → `recompute_confidence`.
- **Nightly cron**: LLM-heavy jobs only, to control cost the way `llm_call_logs` metering already implies matters — `refresh_simulated_signals`, `detect_dependencies`, `generate_executive_briefing`, `compute_requirement_volatility`, decision-log staleness pass.
- **Critical prerequisite**: `SimulatedDataset` is seeded once and never updated. Without a `refresh_simulated_signals` job that nudges each payload and writes headline scalars into `metric_snapshots` on schedule, **Resource Risk (#7) and Sentiment (#13) have nothing to trend** — this is not optional polish, it's load-bearing for two features.

---

## Phase 1 — Buildable now (decomposition of existing engines, or single-pass LLM reasoning that doesn't need trend history)

| # | Feature | Reuses | New | Frontend |
|---|---|---|---|---|
| 8 | Delivery Confidence breakdown | `confidence_service.py::_signals()`/`compute_confidence()` — group the 7 existing signals (+ alignment signals) into 6 categories (Requirement/Engineering/Testing/Dependencies/Resource/Customer), weighted sub-average per category | `sub_scores` JSONB column only | Extend confidence panel on `project-overview-content.tsx`; add `sub_scores` to `ConfidenceOut` in `routers/confidence.py` |
| 10 | AI Judge | `analysis_service.py`, existing judge-pattern in `confidence_judge_messages` | `judge_service.py::review_analysis()`, `prompts.judge_review_messages()`, `ai_judge_reviews` table, `POST /projects/{id}/analysis/{analysis_id}/judge` | "Verify with AI Judge" action on `analysis-content.tsx` tabs |
| 9 | AI Executive Briefing | `analysis_service.py` with existing `AnalysisKind.executive` — mostly packaging | Enrich executive prompt with confidence delta (compare last 2 `ConfidenceScore` rows), scope-change % (from `metric_snapshots`), literal intervene/no-intervene field; run nightly via cron instead of on-demand only | Executive tab gets "auto-generated, last run at X" banner |
| 7 | Resource Risk | `ConnectorType.resource` SimulatedDataset (`team_size`, `utilization_pct`, `developers[]` already shaped) via `retrieval.py::simulated_signals()` | `resource_service.py::compute_resource_risk()`, shares `knowledge_service.py` with #12, new `GET /projects/{id}/resources` | Replace `/resources` placeholder |
| 12 | Knowledge Gap Detection | `Story.labels` + `Story.assignee` (already exist) | `knowledge_service.py::compute_knowledge_map()` (group by module × assignee, flag sole holders), `knowledge_map` table, `prompts.knowledge_gap_messages()` | Same `/resources` page — "Knowledge Concentration" section |
| 3 | Requirement Drift Detection | `retrieval.py::_doc_requirements()` logic becomes the seed for `requirement_items`; same semantic-match approach `alignment_service.py` already uses | `requirement_service.py::sync_requirement_catalog()` (runs after each document extraction), `prompts.requirement_diff_messages()`, `GET /projects/{id}/requirements/drift` | New panel on documents page or overview's alignment panel — lists `status=missing` items with effort/risk |
| 4 | Hidden Dependency Detection | `retrieval.build_context()` (stories, documents, blockers) + Teams/Slack simulated decisions | `dependency_service.py::detect_dependencies()` (nightly cron, LLM cost-controlled), `prompts.dependency_messages()`, `dependency_edges` table, `GET /projects/{id}/dependencies` | `/projects/[id]/risks` (already a near-term "Week 4" stub, not a future placeholder) — simple chain list for v1, not a full graph widget |

Note: #3 and #4 need at minimum 1–2 uploaded documents to produce anything meaningful, but that's a data-availability condition already met by the existing documents feature — no new sync cycles required, so they stay Phase 1.

---

## Phase 2 — Needs the new history infra to accumulate real trend data (a few sync cycles / sprints / refresh cycles deep)

Same shape as the existing constraint in `confidence_service.py::_signals()`, where `velocity_stability` only computes meaningfully once `len(closed) >= 2` — everything here inherits that "needs ≥2 data points" gate.

| # | Feature | Reuses | New | Frontend |
|---|---|---|---|---|
| 1 | Delivery Completion Prediction | Rule+LLM-judge blend pattern from `confidence_service.py` (replicate, don't reinvent) | `prediction_service.py::predict_completion()` — rule part: `remaining_points / avg_velocity` (from `metric_snapshots`) → projected date; LLM part: `prompts.completion_prediction_messages()` → probability/reasons/recommendations; `delivery_predictions` table | New card on project overview next to sprint-progress; cross-sprint view on `/executive` once several sprints exist |
| 2 | Scope Creep Detection | `requirement_items` (Phase 1) + `metric_snapshots` scope counters written every sync | `scope_service.py::compute_scope_creep()` — diff current stories/requirements against baseline snapshot, LLM-estimate schedule/cost impact via `prompts.scope_creep_messages()` | New dashboard panel (scope growth %, new stories, requirements modified, decisions, impact) — good `dataviz` candidate |
| 5 | Requirement Volatility Score | `requirement_items` supersede/edit counts, new `Story.reopened_count`, `metric_snapshots` | `volatility_service.py::compute_volatility()` — weighted 0–100 stability score, itself written back to `metric_snapshots` so it's trendable | Stat tile on overview; feeds #8's Requirement sub-score |
| 6 | Customer Decision Delay | Teams simulated `decisions`/transcript `decisions`+`action_items` | `decision_service.py::sync_decision_log()`, `decision_log` table. **Hard prerequisite, not just a data-volume wait**: neither the Teams payload nor the transcript extraction schema carries `requested_at`/`decided_at` today — must extend `_DOC_TASK`/`_PAYLOADS[ConnectorType.teams]` to carry dates (and have `refresh_simulated_signals` resolve some pending→approved over time) before delay days are real | Table on `/projects/[id]/risks` or analysis page |
| 13 | Stakeholder Sentiment (trend) | `sentiment` SimulatedDataset already has `score/trend/series[]` (static view is Phase-1-cheap to ship) | Real version needs `refresh_simulated_signals` to have run ≥2x so `metric_snapshots` sentiment has a genuine trend, plus `prompts.sentiment_analysis_messages()` reasoning over trend + Teams/Slack highlights + escalation keywords | Replace `/sentiment` placeholder with trend chart + reasons |
| 14 | What-If Simulation | `retrieval.build_context()`, baseline from #1's `delivery_predictions` + latest `ConfidenceScore` | `simulation_service.py::run_what_if()` — LLM-only reasoning, no solver; `prompts.what_if_messages()`; `what_if_scenarios` table; `POST /projects/{id}/simulate` | Cheapest integration: route "what if..." chat questions (extend `CHAT_CAPABILITIES` in `prompts.py`) through existing SSE chat UI; optional structured "Simulate" panel later |

---

## Phase 3 — Long-horizon / cross-tenant data this POC won't have for a while

Both items below are **architecture-ready but data-starved** — nothing here is blocked by missing code, only by row count. Being direct about this now avoids over-promising a demo.

| # | Feature | Status |
|---|---|---|
| 11 | Delivery DNA (flagship, honestly gated) | `Customer.industry` already exists as a grouping key; `Project.status=completed` already exists. Missing: any captured *outcome* once a project closes. **Plan**: create `project_outcomes` stub now + a manual "mark project outcome" affordance in settings so data starts accumulating immediately. **Do not build archetype-matching/probability-of-success logic until there's a real multi-project, multi-industry corpus** — with one org and a handful of seeded projects, any "91% probability of success" number today would be fabricated, not derived. Revisit once real completed-project history exists (this is a multi-month-plus wait, not a sprint). |
| 15 | Portfolio Intelligence | Code is simple aggregation (latest `ConfidenceScore` + `metric_snapshots` scope-growth per project, most-common `blocked_reason`, customer ranking by confidence) and **can ship as soon as Phase 2 features exist** — recommend building the plumbing early since it's cheap. Caveat: with only a few seeded projects under one org, "most common blocker across projects" / "highest-risk customer" will be statistically thin and won't look impressive until tenant count grows. Ship the code, set expectations on the demo. |

New service: `portfolio_service.py::get_portfolio()`, new router `routers/portfolio.py` (`super_admin`-only, per existing role split in `routers/auth.py`), replaces `/portfolio` placeholder.

---

## Cross-Phase Dependency Notes
- **#8** has no upstream dependency — pure decomposition of what `confidence_service.py` already computes. Later features (dependencies via #4, resource via #7/#12, customer via #6/#13) plug into its category buckets as they land.
- **#9** works day one on existing data, gets sharper once #8's sub-scores and #2's scope metric exist.
- **#1** and **#14** both need `metric_snapshots` velocity history (≥2 closed sprints); #14 additionally leans on #1's baseline.
- **#7** and **#12** share one `knowledge_service.py`/`knowledge_map` — build together.
- **#2, #3, #5** all read/write `requirement_items` — build the catalog once, layer creep/drift/volatility on top rather than three parallel extraction paths.
- **#6** is the one Phase 2 item gated by a schema change (transcript/Teams payload needs decision dates), not just data volume — flag this to whoever picks it up.
- **#11 and #15** are gated by tenant/history volume, not code — explicitly backlog/Phase 3 per the user's own framing.
- Real Teams/Slack/email ingestion (replacing `SimulatedDataset` with live OAuth/webhooks) is explicitly out of scope for this plan — a separate future workstream.

## Verification
- Each new service ships with the same pattern already used in the codebase: unit-test the rule-based portion (like `_signals()`), smoke-test the LLM portion against a seeded demo project (`seed_demo_delivery.py`) with `docker compose up`, and confirm cost/tokens land in `llm_call_logs` for every new prompt.
- After each phase, run through the affected frontend page in a browser (Jira-synced demo project) to confirm the placeholder-to-real transition renders correctly in both light/dark theme, per existing UI conventions.
- Migration `003_history_infra.py`: run `alembic upgrade head` against a fresh DB and against the existing seeded DB to confirm both paths work, given migration `002` was itself a fix for an enum-length issue that `create_all` created — verify new enum columns in this migration all specify explicit `length=`.
