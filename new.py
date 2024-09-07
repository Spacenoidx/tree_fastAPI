from fastapi import FastAPI, HTTPException, Request, Query, logger
from pydantic import BaseModel
from enum import Enum
import db_driver

app = FastAPI()

class Category(Enum):
    TOOLS = "tools"
    CONSUMABLES = "consumables"
    TESTING = "testing"
    SOFTWOOD = "Softwood".casefold()
    HARDWOOD = "Hardwood".casefold()

class Item(BaseModel):
    species: str
    meters: float
    feet: float
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
        items = [Item(species=i.species, id=i.id, meters=i.meters, feet=i.feet, category="testing") for i in results]
        return items
    except Exception as e:
        return {"error": str(e)}

@app.get("/items/{item_id}")
def get_item(item_id: int) -> Item:
    """
    Retrieves a specific tree item by its ID from the database.

    Args:
        item_id (int): The unique identifier of the tree item.

    Returns:
        Item: An Item object representing the retrieved tree, or an error message
                if the item is not found.
    """

    try:
        # Query the database for the specific item
        item = db_driver.session.query(db_driver.tree_table).filter_by(id=item_id).first()
        current_item = Item(species=item.species, id=item.id, meters=item.meters, feet=item.feet, category="testing")

        if not item:
            # Raise an HTTPException if not found
            raise HTTPException(status_code=404, detail="Item not found")

        # Return the retrieved item as an Item object
        return current_item

    except Exception as e:
        # Handle other exceptions and return an error message
        return {"error": str(e)}

@app.post("/items/")
def create_item(item: Item):
    with db_driver.Session(db_driver.engine) as session:
        results = session.query(db_driver.tree_table).all()
        item_id = str(len(results))
        new_tree = db_driver.Tree(species=item.species, meters=item.meters, feet=item.feet, category=str(item.category.value))
        session.add(new_tree)
        session.commit()
    return {"message": "Item created successfully"}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    with db_driver.Session(db_driver.engine) as session:
        tree = session.query(db_driver.Tree).filter_by(id=item_id).first()
        if not tree:
            raise HTTPException(status_code=404, detail="Item not found")

        # Log update values
        # logger.info(f"Updating item {item_id} with: species - {item.species}, meters - {item.meters}, feet - {item.feet}, category - {item.category.value}")

        tree.species = item.species
        tree.meters = item.meters
        tree.feet = item.feet
        tree.category = str(item.category.value)

        session.commit()

        # Log update attempt
        # logger.info(f"Item {item_id} updated successfully (committed)")

    return {"message": "Item updated successfully"}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """
    Deletes a specific tree item from the database based on its ID.

    Args:
        item_id (int): The unique identifier of the tree item to delete.

    Returns:
        dict: A message indicating successful deletion.
    """

    with db_driver.Session(db_driver.engine) as session:
        # Query for the item using its ID
        tree = session.query(db_driver.Tree).filter_by(id=item_id).first()

        if not tree:
            # Raise HTTPException if not found
            raise HTTPException(status_code=404, detail="Item not found")

        # Delete the retrieved item (mapped model instance)
        session.delete(tree)
        session.commit()

    return {"message": "Item deleted successfully"}
if __name__  == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)