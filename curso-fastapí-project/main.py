from zoneinfo import ZoneInfo
from fastapi import FastAPI
import time

app = FastAPI()

@app.get("/")
async def root():
    return {"Message": "Hello, World"}

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}

@app.get("/time/{iso_code}/{format}")
async def time_now(iso_code: str, format:str):
    iso =iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = str(ZoneInfo(timezone_str))
    time_now = time.localtime()
    # http://localhost:8000/time/co/24
    if format == "24":
        formatted_time = time.strftime("%H:%M:%S", time_now)
        return {"Time": formatted_time, "Zone": tz}
    # http://localhost:8000/time/co/12
    if format == "12":
        formatted_time_am_pm = time.strftime("%I:%M:%S %p", time_now)
        return {"Time": formatted_time_am_pm, "Zone": tz}
    