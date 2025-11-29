from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.calculation import Calculation
from app.schemas.calculation import CalculationCreate, CalculationRead

router = APIRouter(prefix="/calculations", tags=["calculations"])


@router.get("/", response_model=list[CalculationRead])
def browse(db: Session = Depends(get_db)):
    return db.query(Calculation).all()


@router.post("/", response_model=CalculationRead, status_code=201)
def create(payload: CalculationCreate, db: Session = Depends(get_db)):
    try:
        result = Calculation.compute(payload.a, payload.b, payload.operation)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    calc = Calculation(
        a=payload.a,
        b=payload.b,
        operation=payload.operation,
        result=result,
    )

    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc


@router.get("/{id}", response_model=CalculationRead)
def read(id: int, db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Not found")
    return calc


@router.put("/{id}", response_model=CalculationRead)
def update(id: int, payload: CalculationCreate, db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Not found")

    try:
        calc.result = Calculation.compute(payload.a, payload.b, payload.operation)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    calc.a = payload.a
    calc.b = payload.b
    calc.operation = payload.operation

    db.commit()
    return calc


@router.delete("/{id}", status_code=204)
def delete(id: int, db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(calc)
    db.commit()
