from fastapi import FastAPI,Depends , HTTPException ,status
from app.database.database import products as product_list , categories_db as catagory_list
from app.models.models import Product , Catagories ,ProductCreate ,CategoryEnum,category_map
from app.database.database_config import SessionLocal
from sqlalchemy.orm import Session 
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.schemas import Product as ProductSchema , Category as CategorySchema
from app.routes.product_routes import router as product_router 
from app.routes.catagory_routes import router as category_router
app = FastAPI()
app.include_router(category_router)
app.include_router(product_router)



@app.get("/")
def home():
    return {"message": "Hello FastAPI"}