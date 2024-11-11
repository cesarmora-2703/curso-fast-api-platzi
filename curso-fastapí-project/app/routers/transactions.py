from fastapi import APIRouter

from models import Transaction

router = APIRouter()

@router.post("/transactions", tags=['transactions'])  # Metodo cambiado de get a post
async def create_transaction(transaction_data: Transaction):
    return transaction_data