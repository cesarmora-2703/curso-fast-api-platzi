from sqlmodel import Session

from db import engine
from models import Customer, Transaction

session = Session(engine)
""" customer = Customer(
    name="Dick Grayson",
    description="Robin",
    email="robin@cmartinez.com",
    age=23,
)
session.add(customer)
session.commit()
session.refresh(customer) """

for x in range(200, 300):
    print(f"counter {x}")
    transaction = Transaction(
        customer_id=9,
        description=f"Test number {x}",
        ammount=10 * x,
    )
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
