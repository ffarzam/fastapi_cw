from bson import ObjectId
from fastapi import APIRouter, Depends

from db.mongodb import get_db
from schemas.books import BookOutput, BookInput

routers = APIRouter()


@routers.get("/")
def read_root():
    return {"Hello": "World"}


@routers.get("/items/{item_id}")
async def read_item(item_id: str, db=Depends(get_db)):
    books = db["book"]
    result = await books.find({"_id": ObjectId(item_id)})

    if result:
        book = BookOutput(id=str(result["_id"]), name=result["name"], price=result["price"])
        return book


@routers.patch("/items/{item_id}")
async def update_item(book: BookOutput, db=Depends(get_db)):
    books = db["book"]
    result = await books.update_one({"_id": ObjectId(book.id)},
                                    {"$set": {"name": book.name, "price": book.price}})

    return {"name": book.name, "price": book.price}


@routers.post("/items/")
async def create_item(book: BookInput, db=Depends(get_db)):
    books = db["book"]
    book = book.model_dump()
    result = await books.insert_one(book)
    book_id = str(result.inserted_id)

    return {"book_name": book["name"], "book_price": book["price"], "book_id": book_id}


@routers.delete("/delete/{item_id}")
def delete_item(book_id: str, db=Depends(get_db)):
    books = db["book"]
    books.delete_one({"_id": ObjectId(book_id)})
    return {"book was deleted successfully"}
