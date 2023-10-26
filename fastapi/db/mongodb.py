import motor.motor_asyncio

mongo_url = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
database = client["bookstore"]


def get_db():
    return database

