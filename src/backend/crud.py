from sqlalchemy.orm import Session
from schemas import UserCreate
from utils import get_password_hash
from sqlalchemy import text
from models import Client
from schemas import ClientCreate
import json
from secrets import token_bytes
from datetime import datetime, timedelta

# Function to generate a random salt
def generate_salt(length=16):
    return token_bytes(length).hex()

def create_user(db: Session, user: UserCreate):
    # Check if username is already registered
    check_user_query = text(f"SELECT * FROM users WHERE userName = '{user.username}'")
    result = db.execute(check_user_query).fetchone()
    
    if result:
        raise ValueError("Username already registered")
    
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

    insert_into_passwordhistory_table(db, user.username, hashed_password, salt)
    
    db.commit()  # Commit the transaction
    
    return {"msg": f"User {user.username} registered successfully!"}

def get_user(db: Session, username: str):
    # Fetch user by username, concatenating user input directly into the query (NOT SECURE)
    get_user_query = text(f"SELECT * FROM users WHERE userName = '{username}'")
    
    result = db.execute(get_user_query).fetchone()
    
    return result  # This returns a Row object

BLOCK_DURATION = 90  # Block time in seconds
MAX_ATTEMPTS = 3  # Maximum failed attempts

def validate_user(db: Session, username: str, password: str):
    # Check if the user is blocked
    block_query = text("SELECT failed_attempts, block_until FROM failed_logins WHERE username = :username")
    block_result = db.execute(block_query, {"username": username}).fetchone()

    if block_result:
        failed_attempts, block_until = block_result

        # If user is currently blocked
        if block_until and datetime.now() < block_until:
            remaining_time = (block_until - datetime.now()).total_seconds()
            raise ValueError(f"User is blocked. Please try again in {int(remaining_time)} seconds.")

        # Reset failed attempts after successful login or block expiration
        if block_until and datetime.now() >= block_until:
            reset_attempts_query = text("UPDATE failed_logins SET failed_attempts = 0, block_until = NULL WHERE username = :username")
            db.execute(reset_attempts_query, {"username": username})
            db.commit()

    # Fetch the salt for the username
    salt_query = text("SELECT salt FROM users WHERE userName = :username")
    salt_result = db.execute(salt_query, {"username": username}).fetchone()

    if not salt_result:
        return None  # User does not exist

    salt = salt_result[0]

    # Hash the password with the salt
    hashed_password = get_password_hash(password, salt)

    # Check if the username and hashed password match a user
    query = text("SELECT * FROM users WHERE userName = :username AND password = :hashed_password LIMIT 1")
    result = db.execute(query, {"username": username, "hashed_password": hashed_password}).fetchone()

    if result:
        # Reset failed attempts on successful login
        reset_attempts_query = text("DELETE FROM failed_logins WHERE username = :username")
        db.execute(reset_attempts_query, {"username": username})
        db.commit()
        return True  # User is validated
    else:
        # Increment failed attempts and block the user if necessary
        if block_result:
            failed_attempts += 1
        else:
            failed_attempts = 1

        if failed_attempts >= MAX_ATTEMPTS:
            block_until = datetime.now() + timedelta(seconds=BLOCK_DURATION)
            block_query = text("""
                INSERT INTO failed_logins (username, failed_attempts, block_until)
                VALUES (:username, :failed_attempts, :block_until)
                ON DUPLICATE KEY UPDATE failed_attempts = :failed_attempts, block_until = :block_until
            """)
            db.execute(block_query, {"username": username, "failed_attempts": failed_attempts, "block_until": block_until})
        else:
            block_query = text("""
                INSERT INTO failed_logins (username, failed_attempts)
                VALUES (:username, :failed_attempts)
                ON DUPLICATE KEY UPDATE failed_attempts = :failed_attempts
            """)
            db.execute(block_query, {"username": username, "failed_attempts": failed_attempts})

        db.commit()
        raise ValueError("Invalid username or password")


def verify_password(db: Session, current_password: str, user_name: str) -> bool:

    salt_query = text(f"SELECT salt FROM users WHERE userName = '{user_name}'")
    salt_result = db.execute(salt_query).fetchone()

    if not salt_result:
        # User does not exist, return None or handle appropriately
        return None
    
    password_query = text(f"SELECT password FROM users WHERE userName = '{user_name}'")
    table_password = db.execute(password_query).fetchone()

    salt = salt_result[0]  # Extract the salt from the result tuple

    current_password_after_hash = get_password_hash(current_password, salt)

    if current_password_after_hash == table_password[0]:
        return True
    return False

def get_user_by_name(db: Session, username: str):
    get_user_query = text(f"SELECT * FROM users WHERE userName = '{username}' LIMIT 1;")
    result = db.execute(get_user_query).fetchone()
    return result

def update_password(db: Session, username, new_password: str):

    salt = generate_salt()

    hashed_password = get_password_hash(new_password,salt)

    if not check_password_history(db, username, new_password) :
       return False
        
    
    update_password_query = text("""
    UPDATE users
    SET password = :password , salt = :salt
    WHERE userName = :username
    """)

    # Execute the update query with the new password and salt
    db.execute(update_password_query, {
        "password": hashed_password,
        "salt": salt,
        "username": username 
    })
    db.commit()

    insert_into_passwordhistory_table(db, username, hashed_password, salt)
    return True

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

def insert_into_passwordhistory_table(db: Session, username: str , password: str , salt: str):
    insert_passwordhistory_query = text("""
        INSERT INTO passwordhistory (userName, password, salt)
        VALUES (:username, :password, :salt)
    """)
    
    db.execute(insert_passwordhistory_query, {
        "username": username,
        "password": password,
        "salt": salt
    })
    
    db.commit()  # Commit the transaction

    #Remove the oldest password if there are more than number that i choose in config passwords stored

    # number_of_history = number_of_password_history()

    # clean_up_query = text(f"""
    #     DELETE FROM passwordhistory
    #     WHERE username = '{username}'
    #     AND id NOT IN (
    #         SELECT id FROM passwordhistory
    #         WHERE username = '{username}'
    #         ORDER BY id DESC
    #         LIMIT {number_of_history}
    #     )
    # """)
    
    # db.execute(clean_up_query)
    # db.commit()

def check_password_history(db: Session, username: str, new_password: str) -> bool:
    # Get the user's last passwords hashes from password history
    number_of_history = number_of_password_history()

    password_history_query = text(f"""
    SELECT password, salt FROM passwordhistory
    WHERE username = :username
    ORDER BY id DESC
    LIMIT {number_of_history}
""")
    
    # Fetch last three passwords from the password history
    password_history = db.execute(password_history_query, {"username": username}).fetchall()

    # Check if the new password matches any of the stored passwords
    for record in password_history:
        stored_hashed_password = record['password']
        stored_salt = record['salt']
        new_password_hashed = get_password_hash(new_password, stored_salt)
        # Check if hashed new password matches any of the stored ones
        if stored_hashed_password == new_password_hashed :
            return False
    
    return True  # The new password is valid and hasn't been used before

def number_of_password_history() -> int :
    # Load the config.json file
    with open('config.json', 'r') as file:
        config = json.load(file)

    # Access the "password_history" value
    password_history_value = config['password_history']

    return password_history_value