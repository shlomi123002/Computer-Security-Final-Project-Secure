from sqlalchemy.orm import Session
from schemas import UserCreate
from utils import get_password_hash , check_common_password
from sqlalchemy import text
from schemas import ClientCreate
import json
from secrets import token_bytes
from datetime import datetime, timedelta

# Function to generate a random salt
def generate_salt(length=16):
    return token_bytes(length).hex()

def create_user(db: Session, user: UserCreate):
    # Check if username is already registered (Secure, no SQL injection vulnerability)
    check_user_query = "SELECT * FROM users WHERE userName = :username"
    result = db.execute(text(check_user_query), {"username": user.username}).fetchone()
    
    if result:
        raise ValueError("Username already registered")
    
    if check_common_password(user.password) :
         raise ValueError("common password")
    
    # Insert the new user into the database (Secure, no SQL injection vulnerability)
    salt = generate_salt()
    hashed_password = get_password_hash(user.password, salt)
    insert_user_query = """
        INSERT INTO users (userName, email, password, salt)
        VALUES (:username, :email, :password, :salt)
    """
    db.execute(text(insert_user_query), {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "salt": salt
    })
    insert_into_passwordhistory_table(db, user.username, hashed_password, salt)
    
    db.commit()  # Commit the transaction
    
    return {"msg": f"User {user.username} registered successfully!"}

def get_user(db: Session, username: str):
    # Fetch user by username (Secure, no SQL injection vulnerability)
    get_user_query = "SELECT * FROM users WHERE userName = :username"
    result = db.execute(text(get_user_query), {"username": username}).fetchone()
    
    return result  # This returns a Row object

def number_of_attempts() -> int:
    # Load the config.json file
    with open('config.json', 'r') as file:
        config = json.load(file)
    
    return config['number_of_attempts']

def block_time_in_seconds() -> int:
    # Load the config.json file
    with open('config.json', 'r') as file:
        config = json.load(file)
    
    return config['block_time_in_seconds']

BLOCK_DURATION = block_time_in_seconds()  # Block time in seconds
MAX_ATTEMPTS = number_of_attempts()  # Maximum failed attempts

def validate_user(db: Session, username: str, password: str):
    # Check if the user is blocked (Secure, no SQL injection vulnerability)
    block_query = "SELECT failed_attempts, block_until FROM failed_logins WHERE username = :username ORDER BY id DESC LIMIT 1"
    block_result = db.execute(text(block_query), {"username": username}).fetchone()

    if block_result:
        failed_attempts = block_result[0]
        block_until = block_result[1]

        if block_until and datetime.now() < block_until:
            remaining_time = (block_until - datetime.now()).total_seconds()
            raise ValueError(f"User is blocked. Please try again in {int(remaining_time)} seconds.")

        if block_until and datetime.now() >= block_until:
            reset_attempts_query = "UPDATE failed_logins SET failed_attempts = 0, block_until = NULL WHERE username = :username"
            db.execute(text(reset_attempts_query), {"username": username})
            db.commit()

    # Fetch the salt for the username (Secure, no SQL injection vulnerability)
    salt_query = "SELECT salt FROM users WHERE userName = :username"
    salt_result = db.execute(text(salt_query), {"username": username}).fetchone()

    if not salt_result:
        return None  # User does not exist

    salt = salt_result[0]
    hashed_password = get_password_hash(password, salt)

    # Check if the username and hashed password match a user (Secure, no SQL injection vulnerability)
    query = "SELECT * FROM users WHERE userName = :username AND password = :password LIMIT 1"
    result = db.execute(text(query), {"username": username, "password": hashed_password}).fetchone()

    if result:
        reset_attempts_query = "DELETE FROM failed_logins WHERE username = :username"
        db.execute(text(reset_attempts_query), {"username": username})
        db.commit()
        return True  # User is validated
    else:
        if block_result:
            failed_attempts += 1
        else:
            failed_attempts = 1

        if failed_attempts >= MAX_ATTEMPTS:
            block_until = datetime.now() + timedelta(seconds=BLOCK_DURATION)
            block_query = """
                INSERT INTO failed_logins (username, failed_attempts, block_until)
                VALUES (:username, :failed_attempts, :block_until)
                ON DUPLICATE KEY UPDATE failed_attempts = :failed_attempts, block_until = :block_until
            """
            db.execute(text(block_query), {
                "username": username,
                "failed_attempts": failed_attempts,
                "block_until": block_until
            })
        else:
            block_query = """
                INSERT INTO failed_logins (username, failed_attempts)
                VALUES (:username, :failed_attempts)
                ON DUPLICATE KEY UPDATE failed_attempts = :failed_attempts
            """
            db.execute(text(block_query), {
                "username": username,
                "failed_attempts": failed_attempts
            })

        db.commit()
        raise ValueError("Invalid username or password")

def verify_password(db: Session, current_password: str, user_name: str) -> bool:
    salt_query = "SELECT salt FROM users WHERE userName = :username"
    salt_result = db.execute(text(salt_query), {"username": user_name}).fetchone()

    if not salt_result:
        return None
    
    password_query = "SELECT password FROM users WHERE userName = :username"
    table_password = db.execute(text(password_query), {"username": user_name}).fetchone()

    salt = salt_result[0]
    current_password_after_hash = get_password_hash(current_password, salt)

    return current_password_after_hash == table_password[0]

def get_user_by_name(db: Session, username: str):
    get_user_query = "SELECT * FROM users WHERE userName = :username LIMIT 1"
    result = db.execute(text(get_user_query), {"username": username}).fetchone()
    return result

def update_password(db: Session, username, new_password: str):
    salt = generate_salt()
    hashed_password = get_password_hash(new_password, salt)

    if not check_password_history(db, username, new_password):
        return False

    update_password_query = """
        UPDATE users
        SET password = :password, salt = :salt
        WHERE userName = :username
    """
    db.execute(text(update_password_query), {
        "password": hashed_password,
        "salt": salt,
        "username": username
    })
    db.commit()

    insert_into_passwordhistory_table(db, username, hashed_password, salt)
    return True

def create_client(db: Session, client: ClientCreate):
    client_query = """
        INSERT INTO clients (clientFirstName, clientLastName, clientEmail, clientPhoneNumber)
        VALUES (:first_name, :last_name, :email, :phone)
    """
    db.execute(text(client_query), {
        "first_name": client.clientFirstName,
        "last_name": client.clientLastName,
        "email": client.clientEmail,
        "phone": client.clientPhoneNumber
    })
    db.commit()

    clientID_query = """
        SELECT clientID
        FROM clients
        WHERE clientFirstName = :first_name
        AND clientLastName = :last_name
        AND clientEmail = :email
        AND clientPhoneNumber = :phone
    """
    result = db.execute(text(clientID_query), {
        "first_name": client.clientFirstName,
        "last_name": client.clientLastName,
        "email": client.clientEmail,
        "phone": client.clientPhoneNumber
    }).fetchone()
    clientID = result['clientID']

    insert_into_internet_package(db, client.selectedPackage, clientID)
    insert_into_sectors(db, client.selectedSector, clientID)
    
    return {"message": "Client created successfully"}

def insert_into_sectors(db: Session, sector: str, client_id: str):
    name = sector
    client_query = """
        INSERT INTO sectors (name, client_id)
        VALUES (:name, :client_id)
    """
    db.execute(text(client_query), {
        "name": name,
        "client_id": client_id
    })
    db.commit()

def insert_into_internet_package(db: Session, package: str, clientID: str):
    # Define package details based on the selected package
    if package == "Basic":
        name = "Basic"
        speed = "50 Mbps"
        data_limit = "200GB"
        price = "20$"
    elif package == "Normal":
        name = "Normal"
        speed = "200 Mbps"
        data_limit = "500GB"
        price = "30$"
    elif package == "Premium":
        name = "Premium"
        speed = "400 Mbps"
        data_limit = "1000GB"
        price = "40$"
    else:
        raise ValueError("Invalid package selected")

    # Use a parameterized query to insert the data into the database
    client_query = """
        INSERT INTO internet_packages (client_id, name, speed, data_limit, price)
        VALUES (:clientID, :name, :speed, :data_limit, :price)
    """
    db.execute(text(client_query), {
        "clientID": clientID,
        "name": name,
        "speed": speed,
        "data_limit": data_limit,
        "price": price
    })
    db.commit()

def insert_into_passwordhistory_table(db: Session, username: str, password: str, salt: str):
    insert_passwordhistory_query = """
        INSERT INTO passwordhistory (userName, password, salt)
        VALUES (:username, :password, :salt)
    """
    db.execute(text(insert_passwordhistory_query), {
        "username": username,
        "password": password,
        "salt": salt
    })
    db.commit()

    number_of_history = number_of_password_history()

    clean_up_query = """
        DELETE ph FROM passwordhistory ph
        LEFT JOIN (
            SELECT id FROM passwordhistory
            WHERE userName = :username
            ORDER BY id DESC
            LIMIT :limit_rows
        ) AS keep_rows ON ph.id = keep_rows.id
        WHERE ph.userName = :username
        AND keep_rows.id IS NULL
    """
    db.execute(text(clean_up_query), {
        "username": username,
        "limit_rows": int(number_of_history)
    })
    db.commit()

def check_password_history(db: Session, username: str, new_password: str) -> bool:
    number_of_history = number_of_password_history()

    password_history_query = """
        SELECT password, salt FROM passwordhistory WHERE userName = :username ORDER BY id DESC LIMIT :limit_rows
    """
    password_histories = db.execute(text(password_history_query), {
        "username": username,
        "limit_rows": number_of_history
    }).fetchall()

    for password_entry in password_histories:
        hashed_password = password_entry[0]
        salt = password_entry[1]
        if get_password_hash(new_password, salt) == hashed_password:
            return False

    return True

def number_of_password_history() -> int:
    with open('config.json', 'r') as file:
        config = json.load(file)

    return config['password_history']
