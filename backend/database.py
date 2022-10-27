from models import Item

import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
database = client.Enventory
collection = database.item

async def fetch_all_items():
    items = []
    cursor = collection.find({})
    async for document in cursor:
        items.append(Item(**document))
    return items

async def fetch_item_by_name(name):
    document = await collection.find_one({'name':name})
    return document

async def create_item(item):
    document = item
    result = await collection.insert_one(item)
    return document

async def update_item(name,quantity,image_url):
    await collection.update_one({"name":name},{"$set":{
        "quantity"  : quantity,
        "image_url" : image_url,
    }})
    document = await collection.find_one({'name':name})
    return document

async def remove_item(name):
    await collection.delete_one({'name':name})
    return True