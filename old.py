from fastapi import FastAPI, HTTPException, Request, Query
from pydantic import BaseModel
from enum import Enum
import sqlalchemy
import db_driver

app = FastAPI()

class Category(Enum):
    TOOLS = "tools"
    CONSUMABLES = "consumables"
    TESTING = "testing"
    SOFTWOOD = "softwood"
    HARDWOOD = "hardwood"

class Item(BaseModel):
    name: str
    meters: float
    feet: float
    id: int
    category: Category

@app.get("/")
def get_index() -> list[Item]:
    """
    Fetches all tree data from the database and returns a list of Item objects.

    Returns:
    A list of Item objects representing the tree data, or an error dictionary
        if there's an exception during retrieval.
        """
    try:
        results = db_driver.session.query(db_driver.tree_table).all()
        items = [Item(name=i.species, id=i.id, meters=i.Meters, feet=i.Feet, category="testing") for i in results]
        return items
    except Exception as e:
        # Handle database errors
        return {"error": str(e)}

@app.get("/items")
def get_items(item_id: int = Query(None)):
    if item_id is not None:
        item = items.get(str(item_id))
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    else:
        return items
    


@app.post("/items/")
def create_item(item: Item):
    item_id = str(len(items) + 1)
    items[item_id] = item
    return item

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    print("")
    #query tree based on item ID
    tree = db_driver.session.query(db_driver.tree_table).filter_by(id=item_id).first()
    
    #if not found, raise error
    if not tree:
        raise HTTPException(status_code=404, detail="Item not found")
    
    print("Test!")
        
        
        
    # items[item_id] = item
    return tree

@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return {"message": "Item deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)