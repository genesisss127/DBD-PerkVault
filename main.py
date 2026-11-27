
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Dead by Daylight Survivor Perks API",
    description="A RESTful API for managing Dead by Daylight survivor perks.",
)


# ---------------------------------------------------------------------------
# Survivor Perks
# ---------------------------------------------------------------------------

@app.get("/perks/", response_model=list[schemas.PerkResponse], tags=["perks"], summary="List all perks")
def get_perks(db: Session = Depends(get_db)):
    return db.scalars(select(models.Perk).order_by(models.Perk.id)).all()


@app.get("/perks/{perk_id}", response_model=schemas.PerkResponse, tags=["perks"], summary="Get a single perk")
def get_perk(perk_id: int, db: Session = Depends(get_db)):
    perk = db.get(models.Perk, perk_id)
    if perk is None:
        raise HTTPException(status_code=404, detail=f"Perk with ID {perk_id} not found")
    return perk


@app.post("/perks/", response_model=schemas.PerkResponse, status_code=status.HTTP_201_CREATED, tags=["perks"], summary="Create a perk")
def create_perk(payload: schemas.PerkCreate, db: Session = Depends(get_db)):
    perk = models.Perk(**payload.model_dump())
    db.add(perk)
    db.commit()
    db.refresh(perk)
    return perk


@app.put("/perks/{perk_id}", response_model=schemas.PerkResponse, tags=["perks"], summary="Update a perk")
def update_perk(perk_id: int, payload: schemas.PerkUpdate, db: Session = Depends(get_db)):
    perk = db.get(models.Perk, perk_id)
    if perk is None:
        raise HTTPException(status_code=404, detail=f"Perk with ID {perk_id} not found")
    for field, value in payload.model_dump().items():
        setattr(perk, field, value)
    db.commit()
    db.refresh(perk)
    return perk


@app.delete("/perks/{perk_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["perks"], summary="Delete a perk")
def delete_perk(perk_id: int, db: Session = Depends(get_db)):
    perk = db.get(models.Perk, perk_id)
    if perk is None:
        raise HTTPException(status_code=404, detail=f"Perk with ID {perk_id} not found")
    db.delete(perk)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
