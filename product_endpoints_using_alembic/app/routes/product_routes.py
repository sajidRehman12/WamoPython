    
from fastapi import FastAPI,Depends , HTTPException ,status,APIRouter
from app.database.database import products as product_list , categories_db as catagory_list
from app.models.models import Product , Catagories ,ProductCreate ,CategoryEnum,category_map
from app.database.database_config import get_db
from sqlalchemy.orm import Session 
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.schemas import Product as ProductSchema , Category as CategorySchema



router=APIRouter(prefix="/products",tags=["Products Routes"])


@router.get("/")
def products(db: Session = Depends(get_db)):
    try:
        data = db.query(ProductSchema).all()
        return data

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}")
def product(id: int, db: Session = Depends(get_db)):
    try:
        prod = db.query(ProductSchema).filter(ProductSchema.id == id).first()

        if not prod:
            raise HTTPException(status_code=404, detail="Product not found")

        return prod

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def add_product(product: ProductCreate,category:CategoryEnum , db: Session = Depends(get_db)):
    try:

        category_id=category_map[category]
        new_product = ProductSchema(
            name=product.name,
            description=product.description,
            price=product.price,
            quantity=product.quantity,
            category_id=category_id
        )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return {
            "message": "Product added successfully",
            "data": new_product
        }

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}")
def update_product(id: CategoryEnum, product: Product, db: Session = Depends(get_db)):
    prod = db.query(ProductSchema).filter(ProductSchema.id == id).first()
    category_id=category_map[id]

    if not prod:
        return {"error": "Product not found"}

    prod.name = product.name
    prod.description = product.description
    prod.price = product.price
    prod.quantity = product.quantity
    prod.category_id = product.category_id

    db.commit()
    db.refresh(prod)
    return prod

@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    prod = db.query(ProductSchema).filter(ProductSchema.id == id).first()

    if not prod:
        return {"error": "Product not found"}

    db.delete(prod)
    db.commit()

    return {"message": "Product deleted"}

