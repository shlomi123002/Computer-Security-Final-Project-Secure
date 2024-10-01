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
    # Check if username is already registered (Unsecure, SQL injection vulnerability)
    check_user_query = f"SELECT * FROM users WHERE userName = '{user.username}'"
    result = db.execute(text(check_user_query)).fetchone()
    
    if result:
        raise ValueError("Username already registered")
    
    # Insert the new user into the database (Unsecure, SQL injection vulnerability)
    salt = generate_salt()
    hashed_password = get_password_hash(user.password, salt)
    insert_user_query = f"""
        INSERT INTO users (userName, email, password, salt)
        VALUES ('{user.username}', '{user.email}', '{hashed_password}', '{salt}')
    """
    db.execute(text(insert_user_query))
    insert_into_passwordhistory_table(db, user.username, hashed_password, salt)
    
    db.commit()  # Commit the transaction
    
    return {"msg": f"User {user.username} registered successfully!"}

def get_user(db: Session, username: str):
    # Fetch user by username (Unsecure, SQL injection vulnerability)
    get_user_query = f"SELECT * FROM users WHERE userName = '{username}'"
    result = db.execute(text(get_user_query)).fetchone()
    
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
    # Check if the user is blocked (Unsecure, SQL injection vulnerability)
    block_query = f"SELECT failed_attempts, block_until FROM failed_logins WHERE username = '{username}' ORDER BY id DESC LIMIT 1"
    block_result = db.execute(text(block_query)).fetchone()

    if block_result:
        failed_attempts = block_result[0]
        block_until = block_result[1]

        if block_until and datetime.now() < block_until:
            remaining_time = (block_until - datetime.now()).total_seconds()
            raise ValueError(f"User is blocked. Please try again in {int(remaining_time)} seconds.")

        if block_until and datetime.now() >= block_until:
            reset_attempts_query = f"UPDATE failed_logins SET failed_attempts = 0, block_until = NULL WHERE username = '{username}'"
            db.execute(text(reset_attempts_query))
            db.commit()

    # Fetch the salt for the username (Unsecure, SQL injection vulnerability)
    salt_query = f"SELECT salt FROM users WHERE userName = '{username}'"
    salt_result = db.execute(text(salt_query)).fetchone()

    if not salt_result:
        return None  # User does not exist

    salt = salt_result[0]
    hashed_password = get_password_hash(password, salt)

    # Check if the username and hashed password match a user (Unsecure, SQL injection vulnerability)
    query = f"SELECT * FROM users WHERE userName = '{username}' AND password = '{hashed_password}' LIMIT 1"
    result = db.execute(text(query)).fetchone()

    if result:
        reset_attempts_query = f"DELETE FROM failed_logins WHERE username = '{username}'"
        db.execute(text(reset_attempts_query))
        db.commit()
        return True  # User is validated
    else:
        if block_result:
            failed_attempts += 1
        else:
            failed_attempts = 1

        if failed_attempts >= MAX_ATTEMPTS:
            block_until = datetime.now() + timedelta(seconds=BLOCK_DURATION)
            block_query = f"""
                INSERT INTO failed_logins (username, failed_attempts, block_until)
                VALUES ('{username}', {failed_attempts}, '{block_until}')
                ON DUPLICATE KEY UPDATE failed_attempts = {failed_attempts}, block_until = '{block_until}'
            """
            db.execute(text(block_query))
        else:
            block_query = f"""
                INSERT INTO failed_logins (username, failed_attempts)
                VALUES ('{username}', {failed_attempts})
                ON DUPLICATE KEY UPDATE failed_attempts = {failed_attempts}
            """
            db.execute(text(block_query))

        db.commit()
        raise ValueError("Invalid username or password")


def verify_password(db: Session, current_password: str, user_name: str) -> bool:
    salt_query = f"SELECT salt FROM users WHERE userName = '{user_name}'"
    salt_result = db.execute(text(salt_query)).fetchone()

    if not salt_result:
        return None
    
    password_query = f"SELECT password FROM users WHERE userName = '{user_name}'"
    table_password = db.execute(text(password_query)).fetchone()

    salt = salt_result[0]
    current_password_after_hash = get_password_hash(current_password, salt)

    return current_password_after_hash == table_password[0]

def get_user_by_name(db: Session, username: str):
    get_user_query = f"SELECT * FROM users WHERE userName = '{username}' LIMIT 1"
    result = db.execute(text(get_user_query)).fetchone()
    return result

def update_password(db: Session, username, new_password: str):
    salt = generate_salt()
    hashed_password = get_password_hash(new_password, salt)

    if not check_password_history(db, username, new_password):
       return False

    update_password_query = f"""
        UPDATE users
        SET password = '{hashed_password}', salt = '{salt}'
        WHERE userName = '{username}'
    """
    db.execute(text(update_password_query))
    db.commit()

    insert_into_passwordhistory_table(db, username, hashed_password, salt)
    return True

def create_client(db: Session, client: ClientCreate):
    client_query = f"""
        INSERT INTO clients (clientFirstName, clientLastName, clientEmail, clientPhoneNumber)
        VALUES ('{client.clientFirstName}', '{client.clientLastName}', '{client.clientEmail}', '{client.clientPhoneNumber}')
    """
    db.execute(text(client_query))
    db.commit()

    clientID_query = f"""
        SELECT clientID
        FROM clients
        WHERE clientFirstName = '{client.clientFirstName}'
        AND clientLastName = '{client.clientLastName}'
        AND clientEmail = '{client.clientEmail}'
        AND clientPhoneNumber = '{client.clientPhoneNumber}'
    """
    result = db.execute(text(clientID_query)).fetchone()
    clientID = result['clientID']

    insert_into_internet_package(db, client.selectedPackage, clientID)
    insert_into_sectors(db, client.selectedSector, clientID)
    
    return {"message": "Client created successfully"}

def insert_into_sectors(db: Session, sector: str, client_id: str):
    name = sector
    client_query = f"""
        INSERT INTO sectors (name, client_id)
        VALUES ('{name}', '{client_id}')
    """
    db.execute(text(client_query))
    db.commit()

def insert_into_internet_package(db: Session, package: str, clientID: str):
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

    client_query = f"""
        INSERT INTO internet_packages (client_id, name, speed, data_limit, price)
        VALUES ('{clientID}', '{name}', '{speed}', '{data_limit}', '{price}')
    """
    db.execute(text(client_query))
    db.commit()

def insert_into_passwordhistory_table(db: Session, username: str, password: str, salt: str):
    insert_passwordhistory_query = f"""
        INSERT INTO passwordhistory (userName, password, salt)
        VALUES ('{username}', '{password}', '{salt}')
    """
    db.execute(text(insert_passwordhistory_query))
    db.commit()

    number_of_history = number_of_password_history()

    clean_up_query = f"""
        DELETE ph FROM passwordhistory ph
        LEFT JOIN (
            SELECT id FROM passwordhistory
            WHERE username = '{username}'
            ORDER BY id DESC
            LIMIT {int(number_of_history)}
        ) AS keep_rows ON ph.id = keep_rows.id
        WHERE ph.username = '{username}'
        AND keep_rows.id IS NULL
    """
    db.execute(text(clean_up_query))
    db.commit()

def check_password_history(db: Session, username: str, new_password: str) -> bool:
    number_of_history = number_of_password_history()

    password_history_query = f"""
        SELECT password, salt FROM passwordhistory WHERE userName = '{username}' ORDER BY id DESC LIMIT {number_of_history}
    """
    password_histories = db.execute(text(password_history_query)).fetchall()

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

def delete_client(db: Session, clientID: str):
    delete_client_query = f"""
        DELETE FROM clients
        WHERE clientID = '{clientID}'
    """
    db.execute(text(delete_client_query))
    db.commit()

def update_client(db: Session, client: Client):
    update_client_query = f"""
        UPDATE clients
        SET clientFirstName = '{client.clientFirstName}', clientLastName = '{client.clientLastName}', clientEmail = '{client.clientEmail}', clientPhoneNumber = '{client.clientPhoneNumber}'
        WHERE clientID = '{client.clientID}'
    """
    db.execute(text(update_client_query))
    db.commit()

    insert_into_internet_package(db, client.selectedPackage, client.clientID)
    insert_into_sectors(db, client.selectedSector, client.clientID)
