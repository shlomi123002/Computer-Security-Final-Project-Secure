from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import UserCreate
from crud import create_user
from database import get_db

user_router = APIRouter()

@user_router.post("/register/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        result = create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result
