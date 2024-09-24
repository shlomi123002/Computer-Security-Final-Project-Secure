from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
from utils import get_password_hash, verify_password
from sqlalchemy import text
from models import Client
from schemas import ClientCreate
from secrets import token_bytes
import hashlib

# Function to generate a random salt
def generate_salt(length=16):
    return token_bytes(length).hex()

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
        INSERT INTO users (userName, email, password, salt)
        VALUES (:username, :email, :password, :salt)
    """)
    salt = generate_salt()
    hashed_password = get_password_hash(user.password, salt)
    db.execute(insert_user_query, {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "salt": salt
    })
    
    db.commit()  # Commit the transaction
    
    return {"msg": f"User {user.username} registered successfully!"}

def get_user(db: Session, username: str):
    # Fetch user by username, concatenating user input directly into the query (NOT SECURE)
    get_user_query = text(f"SELECT * FROM users WHERE userName = '{username}'")
    
    result = db.execute(get_user_query).fetchone()
    
    return result  # This returns a Row object

def validate_user(db: Session, username: str, password: str):
    # Fetch the salt for the username
    salt_query = text("SELECT salt FROM users WHERE userName = :username")
    salt_result = db.execute(salt_query, {"username": username}).fetchone()

    if not salt_result:
        # User does not exist, return None or handle appropriately
        return None

    salt = salt_result[0]  # Extract the salt from the result tuple

    # Hash the password with the salt
    hashed_password = get_password_hash(password,salt)

    # Check if the username and hashed password match a user
    query = text(f"SELECT * FROM users WHERE userName = '{username}' AND password = '{hashed_password}' LIMIT 1")
    result = db.execute(query).fetchone()

    if result:
        return True  # User is validated
    else:
        raise ValueError("Invalid username or password")

# sql injection -> admin' OR 1=1 #


def get_user_by_name(db: Session, user_name: str):
    return db.query(User).filter(User.userName == user_name).first()

def get_user_by_email(db: Session, user_email: str):
    return db.query(User).filter(User.email == user_email).first()

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