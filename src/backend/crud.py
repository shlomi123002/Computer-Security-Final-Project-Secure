from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
from utils import get_password_hash

def create_user(db: Session, user: UserCreate):
    db_user = db.query(User).filter(User.userName == user.username).first()
    if db_user:
        raise ValueError("Username already registered")
    
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        raise ValueError("Email already registered")
    
    user_obj = User(
        userName=user.username,
        email=user.email,
        password=get_password_hash(user.password)  # Make sure to hash the password
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    
    return {"msg": f"User {user.username} registered successfully!"}
