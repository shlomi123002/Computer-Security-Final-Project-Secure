from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
from utils import get_password_hash, verify_password
from sqlalchemy import text
from models import Client
from schemas import ClientCreate

def create_user(db: Session, user: UserCreate):
    # Check if username is already registered
    check_user_query = text("SELECT * FROM users WHERE userName = :username")
    result = db.execute(check_user_query, {"username": user.username}).fetchone()
    
    if result:
        raise ValueError("Username already registered")
    
    # Check if email is already registered
    check_email_query = text("SELECT * FROM users WHERE email = :email")
    result = db.execute(check_email_query, {"email": user.email}).fetchone()
    
    if result:
        raise ValueError("Email already registered")
    
    # Insert the new user into the database
    insert_user_query = text("""
        INSERT INTO users (userName, email, password)
        VALUES (:username, :email, :password)
    """)
    hashed_password = get_password_hash(user.password)
    db.execute(insert_user_query, {
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    })
    
    db.commit()  # Commit the transaction
    
    return {"msg": f"User {user.username} registered successfully!"}

def get_user(db: Session, username: str):
    # Fetch user by username
    get_user_query = text("SELECT * FROM users WHERE userName = :username")
    result = db.execute(get_user_query, {"username": username}).fetchone()
    
    return result  # This returns a Row object

def validate_user(db: Session, username: str, password: str):
    # Fetch user by username
    user = get_user(db, username)
    
    if user and verify_password(password, user["password"]):  # Access 'password' from the Row object
        return user
    return None


def get_user_by_name(db: Session, user_name: str):
    return db.query(User).filter(User.userName == user_name).first()

def update_password(db: Session, user: User, new_password: str):
    hashed_password = get_password_hash(new_password)
    user.password = hashed_password
    user.recovery_code = None  # Clear recovery code after password reset
    db.commit()

def create_client(db: Session, client: ClientCreate):
    db_client = Client(
        userName=client.userName,
        clientFirstName=client.clientFirstName,
        clientLastName=client.clientLastName,
        clientPhoneNumber=client.clientPhoneNumber,
        clientEmail=client.clientEmail
    )
    
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    
    return db_client