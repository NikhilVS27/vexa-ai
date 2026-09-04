from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import SessionLocal
from backend.app.models.brand import Brand
from backend.app.schemas.brand import BrandCreate, BrandResponse


router = APIRouter(prefix="/brands", tags=["Brands"])


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=BrandResponse)
def create_brand(
    brand: BrandCreate,
    db: Session = Depends(get_db)
):
    new_brand = Brand(
        name=brand.name,
        website=brand.website,
        industry=brand.industry,
        description=brand.description,
        gaming_history=brand.gaming_history,
        marketing_activity=brand.marketing_activity,
    )

    db.add(new_brand)
    db.commit()
    db.refresh(new_brand)

    return new_brand


@router.get("/", response_model=list[BrandResponse])
def get_brands(db: Session = Depends(get_db)):
    return db.query(Brand).all()