from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from models import Autos  

# Configuración de la URL de la base de datos PostgreSQL
DATABASE_URL = "postgres://user:0m3WSxRjdRQMzFF28tWCyd2YoLBmyyXf@dpg-cscu2olumphs7399dqog-a.oregon-postgres.render.com/db_agenda_sd8j_u7mn"

# FastAPI app
app = FastAPI()

# Pydantic model para los datos de Personas
class AutoCreate(BaseModel):
    matricula: str
    modelo: str
    marca: str
    color: str
    motor: str

class AutoResponse(BaseModel):
    id_auto: int
    matricula: str
    modelo: str
    marca: str
    color: str
    motor: str


@app.post("/autos/", response_model=AutoCreate)
async def crear_auto(auto: AutoCreate):
    try:
        db_auto = await Autos.create(matricula=auto.matricula, modelo=auto.modelo, marca=auto.marca, color=auto.color, motor=auto.motor)
        return AutoResponse(id_auto=db_auto.id_auto, matricula=db_auto.matricula, modelo=db_auto.modelo, marca=db_auto.marca, color=db_auto.color, motor=db_auto.motor)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/autos/", response_model=List[AutoResponse])
async def obtener_autos():
    autos = await Autos.all()
    return [AutoResponse(id_auto=p.id_auto, matricula=p.matricula, modelo=p.modelo, marca=p.marca, color=p.color, motor=p.motor) for p in autos]

@app.on_event("startup")
async def init():
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={"models": ["models"]},  
    )
    await Tortoise.generate_schemas()

@app.on_event("shutdown")
async def shutdown():
    await Tortoise.close_connections()

# Configuración de Tortoise ORM con FastAPI
register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["models"]},  
    generate_schemas=False,
    add_exception_handlers=True,
)


# uvicorn app.main:app --reload