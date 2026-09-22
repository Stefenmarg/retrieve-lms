from core.config import settings
from core.database import Base, SessionLocal, engine
from fastapi import FastAPI
from router.loader import router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)


@app.get("/api/health")
def read_root():
    with engine.connect() as conn:
        conn.exec_driver_sql("SELECT 1")
    return {"status": "ok"}
