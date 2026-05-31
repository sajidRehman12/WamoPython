    
from fastapi import FastAPI,Depends , HTTPException ,status,APIRouter
from app.models.models import Product , Catagories ,ProductCreate ,CategoryEnum,category_map
from app.database.database_config import get_db
from sqlalchemy.orm import Session 
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.schemas import Product as ProductSchema , Category as CategorySchema



router=APIRouter(prefix="/categories",tags=["Categories Routes"])

@router.get("/")
def catagories(db: Session = Depends(get_db)):
    try:
        cat = db.query(CategorySchema).all()
        return cat

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def add_category(catagory: Catagories, db: Session = Depends(get_db)):
    try:
        cat = CategorySchema(
            name=catagory.name,
            description=catagory.description
        )

        db.add(cat)
        db.commit()
        db.refresh(cat)

        return {
            "message": "Category added successfully",
            "data": cat
        }

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Something went wrong: {str(e)}"
        )

@router.put("/{id}")
def update_category(id: int, category: Catagories, db: Session = Depends(get_db)):
    cat = db.query(CategorySchema).filter(CategorySchema.id == id).first()

    if not cat:
        return {"error": "Category not found"}

    cat.name = category.name
    cat.description = category.description

    db.commit()
    db.refresh(cat)
    return cat

@router.delete("/{id}")
def delete_category(id: int, db: Session = Depends(get_db)):
    cat = db.query(CategorySchema).filter(CategorySchema.id == id).first()

    if not cat:
        return {"error": "Category not found"}

    db.delete(cat)
    db.commit()

    return {"message": "Category deleted"}
