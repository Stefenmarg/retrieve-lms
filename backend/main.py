from src.modules.configs import settings
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def read_root():
    return {"status": "ok"}
