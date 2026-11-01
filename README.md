# FastAPI Items API

A small FastAPI application for creating, viewing, updating, and deleting
items. Each item has a required `text` field and an optional `is_done` field.

## Requirements

- Python 3.10 or later
- Windows PowerShell

## Set up and run

From the project directory, create a virtual environment if you do not already
have one, install the dependencies, and start the development server:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

If `.venv` already exists, you can skip the first command. Keep the terminal
running while you use the API. Stop the server with **Ctrl+C**.

The API is available at <http://127.0.0.1:8000>.

## Interactive API documentation

Open <http://127.0.0.1:8000/docs> to try the endpoints in Swagger UI. Expand an
endpoint, click **Try it out**, enter any required values, and click
**Execute**.

If `/docs` is blank, try refreshing with **Ctrl+F5** or opening
<http://127.0.0.1:8000/redoc>. The raw OpenAPI schema is at
<http://127.0.0.1:8000/openapi.json>. If the schema loads but the interactive
docs do not, the browser or network may be blocking Swagger UI's external
assets.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Returns a welcome message. |
| `GET` | `/health` | Liveness probe for the hosting platform. |
| `POST` | `/items` | Adds an item from a JSON request body. |
| `GET` | `/items?limit=10` | Returns up to `limit` items (10 by default). |
| `GET` | `/items/{item_id}` | Returns the item at a zero-based list index. |
| `PUT` | `/items/{item_id}` | Replaces an item at the zero-based list index. |
| `DELETE` | `/items/{item_id}` | Deletes and returns the item at the zero-based list index. |

### Add an item

In PowerShell, run:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/items" -H "Content-Type: application/json" -d '{"text":"apple"}'
```

The request body is JSON. `text` is the item's text, and `is_done` is optional
and defaults to `false`. For example:

```json
{
  "text": "apple",
  "is_done": false
}
```

The response contains the current list of items. Send another POST request
with `"text":"banana"` to add a second item.

### List items

```powershell
curl.exe "http://127.0.0.1:8000/items?limit=3"
```

### Get one item

Item IDs are zero-based, so `0` is the first item:

```powershell
curl.exe "http://127.0.0.1:8000/items/0"
```

If the index does not exist, the API returns a `404` error.

### Update an item

`PUT` replaces the full item. Include both fields; `is_done` defaults to
`false` if omitted:

```powershell
curl.exe -X PUT "http://127.0.0.1:8000/items/0" -H "Content-Type: application/json" -d '{"text":"green apple","is_done":true}'
```

### Delete an item

```powershell
curl.exe -X DELETE "http://127.0.0.1:8000/items/0"
```

The response contains the deleted item. Deleting an item shifts the indexes of
subsequent items, since IDs are zero-based positions in the in-memory list.

## Data storage

Items are kept in memory while the server is running. They are cleared when the
server restarts; this example does not save items to a file or database.

> **Production note:** in-memory storage is not durable and is not shared
> between multiple workers or instances. Render restarts and redeploys clear
> all items. For durable data, back the CRUD operations with PostgreSQL (for
> example with SQLAlchemy and Render Postgres) or attach a persistent disk and
> use SQLite.

## Deploy to Render

The repo includes a `render.yaml` blueprint and a pinned `requirements.txt`, so
the service can be created from the Render Dashboard or from the blueprint.

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

The Python version is pinned to `3.14.8` in `.python-version` (and in
`render.yaml` via `PYTHON_VERSION`). Change both files to upgrade it.

### Option B: Blueprint

1. Push this repository to GitHub.
2. In the Render Dashboard, choose **New > Blueprint**.
3. Select the repository. Render reads `render.yaml` and creates the service
   with the build command, start command, region, and health check already set.

### Verify the deployment

After the deploy finishes, open the service URL:

- `GET /health` should return `{"status":"ok"}`.
- `GET /docs` opens the interactive Swagger UI.
- `GET /` should return `{"message":"Hello, World!"}`.

Example against the live service:

```powershell
curl.exe "https://<your-service>.onrender.com/health"
curl.exe -X POST "https://<your-service>.onrender.com/items" -H "Content-Type: application/json" -d '{"text":"apple"}'
curl.exe "https://<your-service>.onrender.com/items"
```

Free instances spin down after a period of inactivity, so the first request
after idle time may take several seconds while the instance starts.

