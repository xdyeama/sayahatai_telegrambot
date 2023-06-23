import motor.motor_asyncio
import config
from datetime import datetime


cluster = motor.motor_asyncio.AsyncIOMotorClient(config.MONGO_URL)
collection = cluster.sayahatai.users


async def add_user(user_id):
    check = await collection.find_one({"_id": user_id})
    if check:
        return
    payload = {
        "_id": user_id,
        "created_at": datetime.utcnow(),
        "balance": 0,
        "prev_request": "",
        "prev_response": "",
    }
    collection.insert_one(payload)


async def get_request_response(user_id):
    user = await collection.find_one({"_id": user_id})
    return user["prev_request"], user["prev_response"]


async def update_request_response(user_id, new_request, new_response):
    collection.update_one(
        filter={"_id": user_id},
        update={
            "$set": {"prev_request": new_request, 
                     "prev_response": new_response}
        },
    )


async def check_balance(user_id):
    user = await collection.find_one({"_id": user_id})
    return user["balance"] < 50000


async def get_balance(user_id):
    user = await collection.find_one({"_id": user_id})
    return user["balance"]


async def update_balance(user_id, tokens_cnt):
    user = await collection.find_one({"_id": user_id})
    new_balance = user["balance"] + tokens_cnt
    collection.update_one(
        filter={"_id": user_id},
        update={"$set": {"balance": new_balance}},
    )
