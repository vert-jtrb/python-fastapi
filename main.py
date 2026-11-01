from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI(
    title="FastAPI Items API",
    version="1.0.0",
    description="A small CRUD API for managing items.",
)

items: list["Item"] = []

class Item(BaseModel):
    text: str
    is_done: bool = False


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    """Redirect the root URL to the interactive API documentation."""
    return RedirectResponse(url="/docs")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe used by Render health checks."""
    return {"status": "ok"}


@app.post("/items")
def create_item(item: Item) -> list[Item]:
    items.append(item)
    return items


@app.get("/items", response_model=list[Item])
def list_items(limit: int = Query(default=10, ge=0)) -> list[Item]:
    return items[:limit]

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    if 0 <= item_id < len(items):
        return items[item_id]
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item) -> Item:
    if 0 <= item_id < len(items):
        items[item_id] = item
        return item
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int) -> Item:
    if 0 <= item_id < len(items):
        return items.pop(item_id)
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
