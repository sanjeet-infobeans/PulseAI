# PulseAI — Ubuntu 24.04 Setup Guide

Step-by-step instructions to set up and run the entire PulseAI stack on a fresh **Ubuntu 24.04 LTS** machine.

## What you are running

| Service    | Tech                        | Purpose                                  |
|------------|-----------------------------|------------------------------------------|
| `nginx`    | Nginx 1.27                  | Reverse proxy on port **80** (single entrypoint) |
| `frontend` | Next.js 14 (Node 20)        | Web UI                                   |
| `api`      | FastAPI + Uvicorn (Py 3.12) | Backend API, auto-runs DB migrations + seed |
| `postgres` | PostgreSQL 16               | Primary database                         |
| `redis`    | Redis 7                     | Cache / queues                           |

Routing (via Nginx): `http://<host>/` → frontend, `http://<host>/api/` → backend.

External dependencies you must supply:
- **Groq API key** (LLM features) — https://console.groq.com
- **Supabase project** (Postgres + document storage) — optional if you use the bundled local Postgres instead.

---

## Option A — Docker Compose (recommended)

This is the fastest and most reproducible path. Everything runs in containers.

### 1. Update the system

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Docker Engine + Compose plugin

```bash
# Prerequisites
sudo apt install -y ca-certificates curl git

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 3. Run Docker without `sudo` (optional but recommended)

```bash
sudo usermod -aG docker $USER
newgrp docker   # or log out and back in
docker run hello-world   # verify
```

### 4. Get the project onto the machine

```bash
# If using git:
git clone <your-repo-url> PulseAI
cd PulseAI

# Or copy the PulseAI/ directory here via scp/rsync, then:
# cd PulseAI
```

### 5. Configure the backend environment

The API reads its config from `backend/.env`. Create it from the template and fill in real values:

```bash
cp backend/.env.example backend/.env
nano backend/.env
```

Key variables to set:

```dotenv
# --- Database ---
# Use the bundled Postgres container (matches docker-compose defaults):
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/pulseai
# OR point at Supabase (session pooler, port 5432, ssl=require). URL-encode special chars in the password.

# --- Redis (matches compose default password) ---
REDIS_URL=redis://:changeme@redis:6379/0

# --- Security: generate a long random secret ---
SECRET_KEY=<run: openssl rand -hex 32>

# --- Super admin bootstrap (created on first boot) ---
SUPER_ADMIN_EMAIL=admin@infobeans.com
SUPER_ADMIN_PASSWORD=<choose-a-strong-password>
SEED_DEMO_DATA=true

# --- CORS: include the host the browser will use ---
ALLOWED_ORIGINS=http://localhost,http://<server-ip-or-domain>

# --- LLM (required for AI features) ---
GROQ_API_KEY=<your-groq-api-key>

# --- Supabase Storage (only if using document uploads) ---
SUPABASE_URL=<https://xxxx.supabase.co>
SUPABASE_SERVICE_KEY=<service-role-key>
SUPABASE_BUCKET=pulseai-documents

# --- Jira connector (optional) ---
JIRA_TOKEN_ATLAS=<atlassian-api-token>
```

> **Important**
> - When running in Docker Compose, the hostnames are `postgres` and `redis` (the service names), **not** `localhost`.
> - Never commit `backend/.env` — it holds live secrets. Generate `SECRET_KEY` with `openssl rand -hex 32`.

If you want to use the **bundled Postgres/Redis** (no Supabase), also set matching credentials at the compose level. Create a `.env` next to `docker-compose.yml`:

```bash
cat > .env <<'EOF'
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=pulseai
REDIS_PASSWORD=changeme
EOF
```

Make sure these match what you put in `backend/.env` (`DATABASE_URL` / `REDIS_URL`).

### 6. Build and start the stack

```bash
docker compose build
docker compose up -d
```

On first boot the API container automatically:
1. Runs Alembic migrations (`migrations/versions/001_initial.py`).
2. Seeds the super admin + demo data (`SEED_DEMO_DATA=true`).

### 7. Verify

```bash
docker compose ps                 # all services should be "running"/"healthy"
docker compose logs -f api        # watch API startup + migrations
curl http://localhost/api/healthz # should return healthy JSON (db + redis ok)
```

Open the app in a browser:

```
http://<server-ip>/
```

Log in with the `SUPER_ADMIN_EMAIL` / `SUPER_ADMIN_PASSWORD` from `backend/.env`.

### 8. Common Compose operations

```bash
docker compose logs -f            # tail all logs
docker compose restart api        # restart one service
docker compose down               # stop (keeps volumes/data)
docker compose down -v            # stop AND delete DB/redis data
docker compose up -d --build      # rebuild after code changes
```

---

## Option B — Manual / local development (no Docker)

Use this if you want to run the services directly for development.

### 1. Install system dependencies

```bash
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3-pip \
                    postgresql postgresql-contrib redis-server \
                    git curl build-essential libpq-dev
```

### 2. Install Node.js 20 (via NodeSource)

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
node -v && npm -v
```

### 3. Set up PostgreSQL

```bash
sudo systemctl enable --now postgresql
sudo -u postgres psql <<'SQL'
CREATE USER postgres WITH PASSWORD 'postgres';
CREATE DATABASE pulseai OWNER postgres;
SQL
```

### 4. Set up Redis

```bash
sudo systemctl enable --now redis-server
redis-cli ping   # -> PONG
```

### 5. Backend (FastAPI)

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment (localhost hostnames for local run)
cp .env.example .env
nano .env
```

Set for local (note `localhost`, not container names):

```dotenv
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/pulseai
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=<openssl rand -hex 32>
ALLOWED_ORIGINS=http://localhost:3000
GROQ_API_KEY=<your-groq-api-key>
```

Run the API (migrations + seed run automatically on startup):

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# Verify:
curl http://localhost:8000/healthz
```

> Migrations can also be run manually: `alembic upgrade head`

### 6. Frontend (Next.js)

Open a **second terminal**:

```bash
cd frontend
npm ci   # or: npm install
```

Point the frontend at the local API:

```bash
echo 'NEXT_PUBLIC_API_URL=http://localhost:8000' > .env.local
```

Development mode:

```bash
npm run dev        # http://localhost:3000
```

Production mode:

```bash
npm run build
npm start           # http://localhost:3000
```

Open `http://localhost:3000` and log in with the super admin credentials.

---

## Production notes

- **Firewall**: expose only port 80 (and 443 if you add TLS). Postgres (5432) and Redis (6379) are published in the default compose file for convenience — remove those `ports:` mappings in production so they are only reachable inside the Docker network.
- **HTTPS**: put a TLS terminator in front (e.g. Caddy, or Certbot + the existing Nginx). Update `ALLOWED_ORIGINS` and the frontend `NEXT_PUBLIC_API_URL` to your `https://` domain.
- **Secrets**: rotate `SECRET_KEY`, DB/Redis passwords, and API tokens for production. Do not reuse the example values.
- **Backups**: the Postgres data lives in the `postgres_data` Docker volume. Back it up with `docker compose exec postgres pg_dump -U postgres pulseai > backup.sql`.
- **Boot on startup**: Docker's `restart: unless-stopped` policy (already set) restarts containers after a reboot as long as the Docker service is enabled: `sudo systemctl enable docker`.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `docker: permission denied` | Add user to `docker` group (Step 3) and re-login. |
| API unhealthy / DB errors | Check `docker compose logs api`. Verify `DATABASE_URL` host is `postgres` (compose) or `localhost` (manual). |
| `redis ... NOAUTH` | Ensure `REDIS_URL` password matches `REDIS_PASSWORD` in the root `.env`. |
| Frontend can't reach API | Confirm `NEXT_PUBLIC_API_URL` and that Nginx routes `/api/` to the backend. |
| LLM features fail | Set a valid `GROQ_API_KEY`. |
| Port 80 in use | Stop the conflicting service or change the `nginx` port mapping in `docker-compose.yml`. |
| Migrations didn't run | They run on API startup; check `docker compose logs api`, or run `alembic upgrade head` manually (Option B). |
