from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Session, create_engine, select
from models import Band
from typing import List

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session

@app.post("/bands/", response_model=Band)
def create_band(band: Band, session: Session = Depends(get_session)):
    session.add(band)
    session.commit()
    session.refresh(band)
    return band

@app.get("/bands/", response_model=List[Band])
def read_bands(session: Session = Depends(get_session)):
    return session.exec(select(Band)).all()

@app.get("/bands/{band_id}", response_model=Band)
def read_band(band_id: int, session: Session = Depends(get_session)):
    band = session.get(Band, band_id)
    if not band:
        raise HTTPException(status_code=404, detail="Band not found")
    return band

@app.put("/bands/{band_id}", response_model=Band)
def update_band(band_id: int, band: Band, session: Session = Depends(get_session)):
    existing_band = session.get(Band, band_id)
    if not existing_band:
        raise HTTPException(status_code=404, detail="Band not found")
    for key, value in band.dict(exclude_unset=True).items():
        setattr(existing_band, key, value)
    session.add(existing_band)
    session.commit()
    session.refresh(existing_band)
    return existing_band

@app.delete("/bands/{band_id}")
def delete_band(band_id: int, session: Session = Depends(get_session)):
    band = session.get(Band, band_id)
    if not band:
        raise HTTPException(status_code=404, detail="Band not found")
    session.delete(band)
    session.commit()
    return {"detail": "Band deleted"}
