## tech-spec.md  

### 1. Stack  
| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Language** | **Python 3.11** | Rich ecosystem for LLM inference, async HTTP clients, and data processing; easy to ship as a Lambda/Cloud Run function. |
| **Web Framework** | **FastAPI** | High‑performance async, automatic OpenAPI docs, built‑in validation (pydantic) – perfect for an alert‑service API. |
| **Task Scheduler / Workers** | **Celery 5.x** with **Redis** broker | Reliable distributed task queue for periodic health‑checks against external LLM endpoints. |
| **ORM / DB Layer** | **SQLModel** (SQLAlchemy 2 + pydantic) | Declarative models, type‑safe, works with both SQLite (dev) and PostgreSQL (prod). |
| **Runtime** | **Docker** (Alpine‑based) | Guarantees reproducible builds; can be run on any container platform (AWS Fargate, GCP Cloud Run, Azure Container Apps). |
| **CLI / Dev Tools** | **Poetry** for dependency management, **pytest** for unit tests, **ruff** for linting. |

---

### 2. Hosting (Free‑Tier‑First)  

| Component | Preferred Platform | Free‑Tier Details | Production Upgrade |
|-----------|-------------------|-------------------|--------------------|
| **API (FastAPI)** | **Google Cloud Run** (or AWS Fargate) | 2 GiB RAM, 2 vCPU, 2 M requests / month free | Scale to 8 GiB RAM, custom domain, VPC‑peering. |
| **Task Queue (Celery workers)** | **Google Cloud Run (jobs)** or **AWS ECS Fargate Spot** | 0.5 GiB RAM, 1 vCPU, 2 M vCPU‑seconds / month free | Dedicated Fargate/ECS cluster with autoscaling. |
| **Broker (Redis)** | **Redis Cloud (Free tier)** – 30 MB | 30 MB memory, 1 GB egress/month | Upgrade to Redis Enterprise (multi‑AZ, persistence). |
| **Database** | **Supabase (PostgreSQL)** – free tier | 500 MB storage, 2 GB bandwidth | Move to managed Aurora Serverless or CloudSQL. |
| **Observability** | **Grafana Cloud (Free)** – logs & metrics | 50 M logs, 10 k metrics | Grafana Enterprise or Datadog. |
| **Static Assets (OpenAPI UI)** | **GitHub Pages** (auto‑publish from repo) | Unlimited | N/A |

*All components can be run locally with Docker‑Compose for dev/testing.*

---

### 3. Data Model  

| Table / Collection | Key Fields | Description |
|--------------------|------------|-------------|
| **users** | `id (UUID PK)`, `email (unique)`, `hashed_password`, `created_at`, `plan (enum: free, pro)` | Account owners; used for auth & quota. |
| **api_endpoints** | `id (UUID PK)`, `user_id (FK)`, `name`, `base_url`, `api_key_encrypted`, `model_name`, `created_at`, `last_checked_at` | LLM endpoints the user wants monitored. |
| **checks** | `id (UUID PK)`, `endpoint_id (FK)`, `check_type (enum: latency, error_rate, drift)`, `schedule_cron`, `threshold_value`, `enabled` | Definition of each periodic health‑check. |
| **check_results** | `id (UUID PK)`, `check_id (FK)`, `timestamp`, `latency_ms`, `status_code`, `error_flag`, `drift_score (0‑1)`, `alert_sent (bool)` | Raw results stored for audit & trend analysis. |
| **alerts** | `id (UUID PK)`, `check_result_id (FK)`, `channel (enum: email, slack, webhook)`, `payload (JSON)`, `sent_at` | Records of outbound notifications. |
| **secrets** (optional) | `id (UUID PK)`, `user_id (FK)`, `key_name`, `encrypted_value`, `created_at` | Separate store for API keys if not kept in `api_endpoints`. |

*All `*_encrypted` fields use AWS KMS / GCP KMS envelope encryption (see Security).*

---

### 4. API Surface  

| Method | Path | Purpose | Request Body (JSON) | Response |
|--------|------|---------|---------------------|----------|
| **POST** | `/v1/auth/register` | Create new user | `{email, password, plan?}` | `{user_id, token}` |
| **POST** | `/v1/auth/login` | Obtain JWT | `{email, password}` | `{token, expires_in}` |
| **GET** | `/v1/endpoints` | List all monitored endpoints for auth user | – | `[{id, name, model_name, ...}]` |
| **POST** | `/v1/endpoints` | Register a new LLM endpoint to monitor | `{name, base_url, api_key, model_name, checks: [{type, schedule, threshold}]}` | `{endpoint_id}` |
| **PATCH** | `/v1/endpoints/{id}` | Update endpoint config (e.g., add/remove checks) | `{name?, api_key?, checks?}` | `{updated:true}` |
| **DELETE** | `/v1/endpoints/{id}` | Remove endpoint & all its checks | – | `{deleted:true}` |
| **GET** | `/v1/checks/{id}/results?range=24h` | Retrieve recent results for a specific check | – | `{results:[{timestamp, latency_ms, drift_score, ...}]}` |
| **POST** | `/v1/alerts/test` | Send a test alert via selected channel | `{channel, webhook_url?, slack_webhook?, email?}` | `{sent:true}` |
| **GET** | `/v1/health` | Liveness / readiness probe (used by orchestrator) | – | `{status:"ok"}` |

*All endpoints (except `/auth/*` and `/health`) require a Bearer JWT with `sub=user_id`.*

---

### 5. Security Model  

| Aspect | Implementation |
|--------|----------------|
| **Authentication** | **OAuth2 Password Flow** with **JWT** signed by RS256 (private key stored in KMS). Tokens have 1‑hour expiry, refresh via `/auth/refresh`. |
| **Authorization** | Simple RBAC: `user_id` scoped resources; middleware verifies `sub` matches resource owner. Future plans: team‑based orgs with role matrix. |
| **Secrets Management** | API keys are encrypted at rest using **KMS envelope encryption**; ciphertext stored in DB. Decryption occurs in‑memory only during a check. |
| **Transport Security** | Enforced **HTTPS** everywhere (managed TLS by Cloud Run). HTTP Strict Transport Security (HSTS) header set. |
| **Input Validation** | Pydantic models enforce strict typing; all external URLs are validated against a whitelist of schemes (`https`). |
| **Rate Limiting** | Per‑user token bucket (e.g., 100 req/min) via **Redis** middleware. |
| **Audit Logging** | Every auth event, endpoint CRUD, and alert dispatch is logged with user_id, timestamp, and IP. |
| **Compliance** | Data at rest encrypted, minimal PII stored (email hashed for analytics). GDPR‑ready deletion endpoint (`/v1/users/{id}`) to purge all records. |

---

### 6. Observability  

| Signal | Tool / Exporter | Details |
|--------|----------------|---------|
| **Logs** | **Structured JSON** → **Grafana Loki** (via fluent‑bit sidecar) | Include request_id, user_id, endpoint_id, level. |
| **Metrics** | **Prometheus** exporter (FastAPI‑Prometheus) → **Grafana Cloud** | - `api_requests_total{method, path, status}` <br> - `check_execution_seconds{type, outcome}` <br> - `alert_sent_total{channel, result}` |
| **Traces** | **OpenTelemetry** (Python SDK) → **Grafana Tempo** | End‑to‑end trace from API request → Celery task → external LLM call. |
| **Health** | `/v1/health` endpoint + **Cloud Run readiness probes** | Returns DB & Redis connectivity status. |
| **Alerting** | Grafana alert rules on `check_execution_seconds` and `drift_score` thresholds → Slack/email to on‑call. |

---

### 7. Build / CI  

| Stage | Tool | Steps |
|-------|------|-------|
| **Code Checkout** | GitHub Actions | `actions/checkout@v4` |
| **Static Analysis** | `ruff` + `mypy` | Fail on warnings. |
| **Unit Tests** | `pytest` (coverage ≥ 85%) | Run in matrix Python 3.11. |
| **Security Scan** | **Bandit**, **Trivy** (container image) | Block on high severity findings. |
| **Build Docker Image** | `docker/build-push-action` | Tag `ghcr.io/arkashira/llm-pulse:${{github.sha}}` |
| **Push to Registry** | GitHub Container Registry (public for free tier) | |
| **Deploy to Staging** | **Google Cloud Run** (via `gcloud run deploy`) | Deploy on PR merge to `main`. |
| **Smoke Test** | Post‑deployment script hitting `/v1/health` | Abort if non‑200. |
| **Release** | Manual GitHub Release → bump version in `pyproject.toml` | Trigger production deploy via separate workflow (`prod-deploy.yml`). |

*All secrets (KMS keys, DB passwords) are injected via GitHub Encrypted Secrets and accessed at runtime through the platform’s secret manager.*