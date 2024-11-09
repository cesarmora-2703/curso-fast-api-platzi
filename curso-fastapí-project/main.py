from zoneinfo import ZoneInfo
from fastapi import FastAPI
import time

from models import Customer, CustomerCreate, Transaction, Invoice


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
async def time_now(iso_code: str, format: str):
    iso = iso_code.upper()
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


db_customers: list[Customer] = []

@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate):
    customer = Customer.model_validate(customer_data.model_dump())
    # Asumiendo que hace base de datos
    customer.id = len(db_customers)
    db_customers.append(customer)
    return customer
    

@app.get("/customers", response_model=list[Customer])  # Metodo cambiado de get a post
async def list_customer():
    return db_customers

@app.get("/customers/{id}", response_model=Customer)
async def detail_customer(id: int):
    try:
        customer = db_customers[id]
        return customer
    except:
        return None



@app.post("/invoices")  # Metodo cambiado de get a post
async def create_invoice(invoice_data: Invoice):
    return invoice_data


@app.post("/transactions")  # Metodo cambiado de get a post
async def create_transaction(transaction_data: Transaction):
    return transaction_data
