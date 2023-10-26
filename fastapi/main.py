import uvicorn
from fastapi import FastAPI

from routers.accounts import routers as accounts_router
from routers.bookstore import routers as bookstore_router

app = FastAPI()

app.include_router(accounts_router, prefix="/accounts")
app.include_router(bookstore_router, prefix="/bookstore")

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)