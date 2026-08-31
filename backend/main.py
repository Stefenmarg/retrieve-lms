from backend.modules.config import settings
from backend.modules.database import engine, SessionLocal
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def read_root():
    with engine.connect() as conn:
        conn.exec_driver_sql("SELECT 1")
    return {"status": "ok"}
