from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from models import Customer, CustomerCreate, CustomerPlan, CustomerUpdate, Plan
from db import SessionDep

router = APIRouter()


@router.post("/customers", response_model=Customer, tags=["customers"])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@router.get(
    "/customers", response_model=list[Customer], tags=["customers"]
)  # Metodo cambiado de get a post
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all()


@router.get("/customers/{id}", response_model=Customer, tags=["customers"])
async def detail_customer(id: int, session: SessionDep):
    customer = session.get(Customer, id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.delete("/customers/{id}", tags=["customers"])
async def delete_customer(id: int, session: SessionDep):
    customer = session.get(Customer, id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    session.delete(customer)
    session.commit()
    return {"detail": "ok"}


@router.patch(
    "/customers/{id}",
    response_model=Customer,
    status_code=status.HTTP_201_CREATED,
    tags=["customers"],
)
async def update_customer(id: int, customer_data: CustomerUpdate, session: SessionDep):
    customer = session.get(Customer, id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    old_data = customer_data
    update_data = customer_data.model_dump(exclude_unset=True)
    # Revisando cambios de los datos
    if old_data.name != update_data["name"]:
        update_data["name"] = old_data.name
    if old_data.description != update_data["description"]:
        update_data["description"] = old_data.description
    if old_data.email != update_data["email"]:
        update_data["email"] = old_data.email
    if old_data.age != update_data["age"]:
        update_data["age"] = old_data.age

    customer.sqlmodel_update(update_data)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@router.post("/customers/{customer_id}/plans/{plan_id}", tags=["plans"])
async def suscribe_customer_to_plan(
    customer_id: int, plan_id: int, session: SessionDep
):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)
    print(customer_db)
    print(plan_db)
    if not customer_db or not plan_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer or Plan doesn't exist.",
        )

    customer_plan_db = CustomerPlan(plan_id=plan_db.id, customer_id=customer_db.id)
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db


@router.get("/customers/{customer_id}/plans", tags=["customers"])
async def customer_suscribed_to_plan(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)

    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    query = (
        select(CustomerPlan)
        .where(CustomerPlan.customer_id == customer_id)
    )
    plans = session.exec(query).all()
    return plans
