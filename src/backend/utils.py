from passlib.context import CryptContext
from passlib.utils import consteq
from secrets import token_bytes

# Define CryptContext with pbkdf2_sha256
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256"
)

# Function to generate a random salt
def generate_salt(length=16):
    return token_bytes(length).hex()

# Function to hash a password with salt
def get_password_hash(password: str) -> str:
    salt = generate_salt()
    # Hash the password with the salt
    hashed_password = pwd_context.hash(password + salt)
    # Store the salt along with the hashed password
    return f"{salt}${hashed_password}"

# Function to verify a password
def verify_password(stored_password: str, provided_password: str) -> bool:
    # Extract the salt and the hashed password
    salt, hashed_password = stored_password.split('$', 1)
    # Verify the provided password with the extracted salt
    return pwd_context.verify(provided_password + salt, hashed_password)
