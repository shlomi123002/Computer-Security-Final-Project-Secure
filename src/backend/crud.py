from sqlalchemy.orm import Session
from models import User
from utils import get_password_hash
from schemas import UserCreate, UserLogin
from utils import verify_password

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
        #password=get_password_hash(user.password)  # Make sure to hash the password ################## the hashing ###############
        password = user.password 
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    
    return {"msg": f"User {user.username} registered successfully!"}

def get_user(db: Session, username: str):
    return db.query(User).filter(User.userName == username).first()

def validate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if user and verify_password(password, user.password):
        return user
    return None