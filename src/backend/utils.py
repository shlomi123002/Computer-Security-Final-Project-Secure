from passlib.context import CryptContext
from passlib.utils import consteq
from secrets import token_bytes
import random
import smtplib
from email.mime.text import MIMEText

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
    # return f"{salt}${hashed_password}"
    return password

# Function to verify a password
# def verify_password(stored_password: str, provided_password: str) -> bool:
#     # Extract the salt and the hashed password
#     salt, hashed_password = stored_password.split('$', 1)
#     # Verify the provided password with the extracted salt
#     return pwd_context.verify(provided_password + salt, hashed_password)


def verify_password(plain_password: str, database_password: str) -> bool:
    if plain_password == database_password :
        return True
    return False

def send_recovery_code(email: str):
    recovery_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    # Create the email message
    msg = MIMEText(f"Your recovery code is: {recovery_code}")
    msg['Subject'] = 'Password Recovery Code'
    msg['From'] = 'comunicationltdproject2024@gmail.com'
    msg['To'] = email

    try:
        # Connect to the Gmail SMTP server
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login('comunicationltdproject2024@gmail.com', 'zdfv dwpx kqzs xjiu')  # Use app-specific password if needed
        smtp.sendmail('comunicationltdproject2024@gmail.com', email, msg.as_string())
        smtp.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")
    
    return recovery_code