from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Item

app = FastAPI()

origins = ['http://localhost:3000']

from database import(
    fetch_all_items,
    fetch_item_by_name,
    create_item,
    update_item,
    remove_item,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)

@app.get('/')
def index():
    return "Hello world!"

@app.get('/api/item')
async def get_all_items():
    response = await fetch_all_items()
    return response

@app.get('/api/item/{name}', response_model=Item)
async def get_item_by_name(name):
    response = await fetch_item_by_name(name)
    if response:
        return response
    raise HTTPException(404, "Item not found")

@app.post('/api/item', response_model=Item)
async def post_item(item:Item):
    response = await create_item(item.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

@app.put('/api/item/{name}', response_model=Item)
async def put_item(name:str,quantity:int,image_url:str):
    response = await update_item(name, quantity,image_url)
    if response:
        return response
    raise HTTPException(404, "Item not found")

@app.delete('/api/item/{name}')
async def delete_item(name):
    response = await remove_item(name)
    if response:
        return "Item deleted successfully"
    raise HTTPException(400,"Something went wrong")