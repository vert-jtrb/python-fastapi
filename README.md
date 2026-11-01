# FastAPI Items API

A small FastAPI CRUD application for creating, viewing, updating, and deleting
items. Each item has a required `text` field and an optional `is_done` field.

- **Local development:** `uvicorn main:app --reload`
- **Production (Render):** `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Interactive docs:** `/docs`

## Table of contents

- [Overview](#overview)
- [Project structure](#project-structure)
- [Requirements](#requirements)
- [Quick start](#quick-start)
- [Configuration](#configuration)
- [API reference](#api-reference)
- [Data storage](#data-storage)
- [Deploy to Render](#deploy-to-render)
- [Troubleshooting](#troubleshooting)

## Overview

The application exposes a JSON REST API backed by an in-memory list. It is
intended as a small reference service and a starting point for a production
deployment.

| Capability | Details |
| --- | --- |
| Framework | FastAPI |
| ASGI server | Uvicorn |
| Data model | `Item { text: str, is_done: bool = false }` |
| Storage | In-memory list (not persistent) |
| Python version | 3.10+ locally; 3.14.8 on Render |
| Hosting | Render Web Service (Singapore, free plan) |

## Project structure

```text
python-cc/
├── main.py             # FastAPI app, Item model, and CRUD endpoints
├── requirements.txt    # Pinned runtime dependencies for local and Render
├── render.yaml         # Render Blueprint (build, start, region, health check)
├── .python-version     # Python version used by Render (3.14.8)
├── README.md           # This document
└── .gitignore          # Excludes .venv, __pycache__, .env, and tooling output
```

Generated locally and intentionally not committed:

```text
.venv/                  # Virtual environment
__pycache__/            # Python bytecode
.env                    # Local secrets (see .gitignore)
```

### Request flow

```text
Client
  │
  ▼
Uvicorn (ASGI server)
  │
  ▼
FastAPI app (main.py)
  │
  ▼
items: list[Item]  ← in-memory storage
```

## Requirements

- Python 3.10 or later
- `pip`
- Windows PowerShell (commands below use PowerShell syntax)

## Quick start

From the project root, create a virtual environment, install dependencies, and
start the development server:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

If `.venv` already exists, skip the first command. Keep the terminal running
while you use the API. Stop the server with **Ctrl+C**.

The API is available at <http://127.0.0.1:8000>.

> **Tip:** To use a different port, add `--port 8001` to the `uvicorn` command.

### Interactive API documentation

Open <http://127.0.0.1:8000/docs> to try the endpoints in Swagger UI. Expand an
endpoint, click **Try it out**, enter any required values, and click
**Execute**.

The raw OpenAPI schema is at <http://127.0.0.1:8000/openapi.json>, and ReDoc is
at <http://127.0.0.1:8000/redoc>.

## Configuration

The application itself needs no environment variables to run locally. Render
sets the following automatically or through `render.yaml`:

| Variable | Source | Purpose |
| --- | --- | --- |
| `PORT` | Render | Port the start command binds to. |
| `PYTHON_VERSION` | `render.yaml` | Pins Python to `3.14.8`. |
| `ENVIRONMENT` | `render.yaml` | Set to `production` for deployed services. |

The Python version is also pinned in `.python-version`. If you upgrade Python,
update both `.python-version` and the `PYTHON_VERSION` value in `render.yaml`.

## API reference

### Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Returns `{"docs": "/docs"}`, a link to the interactive docs. |
| `GET` | `/health` | Liveness probe used by Render health checks. |
| `POST` | `/items` | Adds an item from a JSON request body. Returns the full list. |
| `GET` | `/items?limit=10` | Returns up to `limit` items (10 by default). |
| `GET` | `/items/{item_id}` | Returns the item at a zero-based list index. |
| `PUT` | `/items/{item_id}` | Replaces the item at the zero-based list index. |
| `DELETE` | `/items/{item_id}` | Deletes and returns the item at the zero-based list index. |

### Item model

```json
{
  "text": "apple",
  "is_done": false
}
```

- `text` is required and must be a string.
- `is_done` is optional and defaults to `false`.
- `item_id` is a zero-based position in the in-memory list, not a permanent
  database ID. Deleting an item shifts the indexes of subsequent items.

### Examples

The examples use PowerShell's `Invoke-RestMethod`. They target the local server
at `http://127.0.0.1:8000`.

**Add an item**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/items" -Method Post `
  -ContentType "application/json" -Body '{"text":"apple"}'
```

The response contains the current list of items. Send another request with
`"text":"banana"` to add a second item.

**List items**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/items?limit=3"
```

**Get one item**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/0"
```

If the index does not exist, the API returns `404`.

**Update an item**

`PUT` replaces the full item. Include both fields; `is_done` defaults to
`false` if omitted:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/0" -Method Put `
  -ContentType "application/json" -Body '{"text":"green apple","is_done":true}'
```

**Delete an item**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/0" -Method Delete
```

The response contains the deleted item.

> **Using curl instead?** On PowerShell, pass the JSON body through a variable
> so the inner quotes survive: `$body = '{"text":"apple"}'` then
> `curl.exe -X POST "http://127.0.0.1:8000/items" -H "Content-Type: application/json" -d $body`.

## Data storage

Items are kept in memory while the server is running. They are cleared when the
server restarts; this example does not save items to a file or database.

> **Production note:** in-memory storage is not durable and is not shared
> between multiple workers or instances. Render restarts and redeploys clear
> all items. For durable data, back the CRUD operations with PostgreSQL (for
> example with SQLAlchemy and Render Postgres) or attach a persistent disk and
> use SQLite.

## Deploy to Render

The repo includes a `render.yaml` Blueprint and a pinned `requirements.txt`, so
the service can be created from the Render Dashboard or from the Blueprint.

### Option A: Render Dashboard (New Web Service)

Use these values when creating the service:

| Setting | Value |
| --- | --- |
| Language | `Python 3` |
| Branch | `main` |
| Region | `Singapore (Southeast Asia)` |
| Root Directory | *(leave empty)* |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Health Check Path | `/health` |

Then click **Deploy web service**. The build installs the pinned dependencies
from `requirements.txt`, and Render supplies the `$PORT` environment variable
to the start command.

> **Important:** do not use the default `gunicorn your_application.wsgi` start
> command. It is for WSGI applications, and FastAPI is an ASGI application.

### Option B: Render Blueprint

1. Push this repository to GitHub.
2. In the Render Dashboard, choose **New > Blueprint**.
3. Select the repository. Render reads `render.yaml` and creates the service
   with the build command, start command, region, and health check already set.

### Verify the deployment

After the deploy finishes, open the service URL:

- `GET /health` should return `{"status":"ok"}`.
- `GET /` should return `{"docs":"/docs"}`.
- `GET /docs` opens the interactive Swagger UI.

Example against the live service:

```powershell
Invoke-RestMethod -Uri "https://<your-service>.onrender.com/health"

$body = '{"text":"apple"}'
Invoke-RestMethod -Uri "https://<your-service>.onrender.com/items" -Method Post `
  -ContentType "application/json" -Body $body

Invoke-RestMethod -Uri "https://<your-service>.onrender.com/items"
```

Free instances spin down after a period of inactivity, so the first request
after idle time may take several seconds while the instance starts.

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'fastapi'` | Dependencies not installed in the active environment. | Run `pip install -r requirements.txt` with the same Python executable you use to start Uvicorn. |
| `[Errno 10048] address already in use` | Another process is using port 8000. | Start with `--port 8001`, or stop the other process. |
| `/docs` is blank | Swagger UI's external assets are blocked. | Refresh with **Ctrl+F5**, or open `/redoc`. If `/openapi.json` loads, the API itself is fine. |
| Render build fails at `pip install` | `requirements.txt` is missing or the Root Directory is wrong. | Keep Root Directory empty and confirm `requirements.txt` is at the repo root. |
| Render deploy fails at start | Wrong start command or Python version. | Use `uvicorn main:app --host 0.0.0.0 --port $PORT` and keep `.python-version` in sync. |
| Render health check fails | `/health` is missing or the app crashed on startup. | Check the Render logs and confirm `GET /health` returns `200`. |
| Data disappears after redeploy | Storage is in-memory. | Expected; add PostgreSQL or a persistent disk for durable data. |
