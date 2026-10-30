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
.\.venv\Scripts\python.exe -m pip install fastapi uvicorn
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
