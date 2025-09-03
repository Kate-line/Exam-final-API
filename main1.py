from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# Modèles de données
class Characteristic(BaseModel):
    max_speed: float
    color: str

class SaveModel(BaseModel):
    identifiant: str
    brand: str
    model: str
    characteristics: Characteristic

# Base de données simulée
db: Dict[str, SaveModel] = {}

# Route GET /ping
@app.get("/ping")
def ping():
    return "pong"

# Route POST /cars
@app.post("/cars", status_code=201)
def add_cars(cars: List[SaveModel]):
    for car in cars:
        db[car.identifiant] = car
    return {"message": "Voitures ajoutées avec succès."}

# Route GET /cars
@app.get("/cars")
def get_all_cars():
    return list(db.values())

# Route GET /cars/{id}
@app.get("/cars/{id}")
def get_car_by_id(id: str):
    if id not in db:
        raise HTTPException(status_code=404, detail="Voiture non trouvée.")
    return db[id]

# Route POST /cars/{id}/characteristics
@app.post("/cars/{id}/characteristics")
def update_characteristics(id: str, characteristics: Characteristic):
    if id not in db:
        raise HTTPException(status_code=404, detail="Voiture non trouvée.")
    try:
        db[id].characteristics = characteristics
        return {"message": "Caractéristiques mises à jour."}
    except Exception:
        raise HTTPException(status_code=400, detail="Objet mal formé.")
