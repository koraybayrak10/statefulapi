import json
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

DATA_FILE = Path("app/storage/data.json")

app = FastAPI(
    title="Stateful API (No DB)",
    description="JSON file based stateful API",
    swagger_ui_parameters={
        "customCssUrl": "/static/swagger.css"
    }
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# --------- MODELS ---------

class Item(BaseModel):
    name: str
    value: int

# --------- HELPERS ---------

def read_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# --------- ROUTES ---------

@app.get("/items")
def get_items():
    return read_data()

@app.post("/items")
def add_item(item: Item):
    data = read_data()
    data["items"].append(item.dict())
    write_data(data)
    return {"message": "Item added", "item": item}

@app.get("/health")
def health():
    return {"status": "stateful-ok"}
