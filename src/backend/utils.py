from passlib.context import CryptContext
import smtplib
import hashlib
import hmac
from email.mime.text import MIMEText

# Define CryptContext with pbkdf2_sha256
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256"
)

# Password hashing function
def get_password_hash(password: str, salt: str) -> str:
    hashed_password = hmac.new(salt.encode(), password.encode(), hashlib.sha256).hexdigest()
    return hashed_password

def send_recovery_code(email: str , recovery_code: str):
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

def recovery_code_hashed(random_code: str , salt: str) -> str :
    random_code_with_salt = salt + random_code 
    # recivery code with salt + sha1 
    recovery_code = hashlib.sha1(random_code_with_salt.encode()).hexdigest()

    return recovery_code

def check_common_password(password : str):
    with open('commonPasswords.txt', 'r') as file:
        for line in file:
            if password in line:
                return True 
    return False 


