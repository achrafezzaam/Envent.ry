from fastapi import UploadFile
from models import Item

# import boto3
# S3_BUCKET_NAME = "s3-bucket-test-achraf-ezzaam"

import motor.motor_asyncio

import os
import aiofiles

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

async def update_item(name,quantity):
    await collection.update_one({"name":name},{"$set":{
        "quantity"  : quantity,
    }})
    document = await collection.find_one({'name':name})
    return document

# async def create_url_link(name, file:UploadFile):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(S3_BUCKET_NAME)

    document = await collection.find_one({'name':name})
    if document["image_url"]:
        filename = document["image_url"].replace("https://{S3_BUCKET_NAME}.s3.amazonaws.com/","")
        bucket.delete_object(Key=filename)
    
    bucket.upload_fileobj(file.file, file.filename, ExtraArgs={"ACL": "public-read"})

    upload_file_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{file.filename}"

    await collection.update_one({"name":name},{"$set":{
        "image_url"  : upload_file_url,
    }})
    document = await collection.find_one({'name':name})
    return document

async def create_url_link(name, file:UploadFile):

    document = await collection.find_one({'name':name})
    if document["image_url"]:
        os.remove(document["image_url"])

    completeName = os.path.join('.\images', file.filename)
    async with aiofiles.open(completeName, 'wb') as out_file:
        content = file.file.read()  # async read chunk
        await out_file.write(content)  # async write chunk

    await collection.update_one({"name":name},{"$set":{
        "image_url"  : completeName,
    }})
    return document

async def remove_item(name):
    await collection.delete_one({'name':name})
    return True