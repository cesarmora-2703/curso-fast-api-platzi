from datetime import datetime, timezone
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"Message": "Hello, World"}

@app.get("/time")
async def time_now():
    return {"Time": datetime.now()}