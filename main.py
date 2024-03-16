from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("index.html", "r") as file:
        html_content = file.read()
    return html_content

# Allowing CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce']
products_collection = db['products']

# Product model
class Product(BaseModel):
    name: str

# Buy endpoint
@app.post("/buy")
async def buy_product(product: dict):
    product_name = product.get('name')
    if products_collection.find_one({"name": product_name}):
        return {"success": True, "message": f"Thank you for purchasing {product_name}!"}
    else:
        # Insert the purchased product into the MongoDB collection
        products_collection.insert_one({"name": product_name})
        return {"success": True, "message": f"Thank you for purchasing {product_name}!"}
