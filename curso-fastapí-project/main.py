from zoneinfo import ZoneInfo
import time

from sqlmodel import select
from fastapi import FastAPI, HTTPException
from models import Customer, CustomerCreate, Transaction, Invoice
from db import SessionDep, create_all_tables

app = FastAPI(lifespan=create_all_tables)


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


@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@app.get("/customers", response_model=list[Customer])  # Metodo cambiado de get a post
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all()


@app.get("/customers/{id}", response_model=Customer)
async def detail_customer(id: int, session: SessionDep) -> Customer:
    customer = session.get(Customer, id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.delete("/customers/{id}")
async def delete_customer(id: int, session: SessionDep) -> Customer:
    customer = session.get(Customer, id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    session.delete(customer)
    session.commit()
    return {"detail": "ok"}

@app.put("/customers/{id}", response_model=Customer)
async def update_customer(id: int, customer_data: CustomerCreate, session: SessionDep) -> Customer:
    customer = session.get(Customer, id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    update_data = customer_data.model_dump(exclude_unset=True)
    customer.sqlmodel_update(update_data)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@app.post("/invoices")  # Metodo cambiado de get a post
async def create_invoice(invoice_data: Invoice):
    return invoice_data


@app.post("/transactions")  # Metodo cambiado de get a post
async def create_transaction(transaction_data: Transaction):
    return transaction_data
