from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.calculation import CalculationCreate, CalculationRead
from app.models.calculation import Calculation
from app.database import get_db

router = APIRouter(prefix="/calculations", tags=["Calculations"])

@router.post("/", response_model=CalculationRead)
def create_calculation(calc: CalculationCreate, db: Session = Depends(get_db)):
    db_calc = Calculation(**calc.dict())
    db.add(db_calc)
    db.commit()
    db.refresh(db_calc)
    return db_calc

@router.get("/", response_model=List[CalculationRead])
def browse_calculations(db: Session = Depends(get_db)):
    return db.query(Calculation).all()

@router.get("/{calc_id}", response_model=CalculationRead)
def read_calculation(calc_id: int, db: Session = Depends(get_db)):
    calc = db.query(Calculation).get(calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc

@router.put("/{calc_id}", response_model=CalculationRead)
def update_calculation(calc_id: int, calc_update: CalculationCreate, db: Session = Depends(get_db)):
    calc = db.query(Calculation).get(calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    for key, value in calc_update.dict().items():
        setattr(calc, key, value)
    db.commit()
    db.refresh(calc)
    return calc

@router.delete("/{calc_id}")
def delete_calculation(calc_id: int, db: Session = Depends(get_db)):
    calc = db.query(Calculation).get(calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    db.delete(calc)
    db.commit()
    return {"detail": "Calculation deleted"}
