from pydantic import BaseModel, validator
import re
import json



def load_json_config():
    with open('config.json', 'r') as file:
        return json.load(file)

json_config = load_json_config()

# Extract configuration values
PASSWORD_MIN_LENGTH = json_config.get('password_min_length', 10)
PASSWORD_UPPERCASE = json_config.get('password_uppercase', True)
PASSWORD_SPECIAL = json_config.get('password_special', True)
PASSWORD_NUMBER = json_config.get('password_number', True)


@validator('password')
def validate_password(cls, value):
    errors = []
    if len(value) < 10:
        errors.append('Password must be at least 10 characters long')
    if not re.search(r'[A-Z]', value):
        errors.append('Password must contain at least one uppercase letter')
    if not re.search(r'\d', value):
        errors.append('Password must contain at least one number')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        errors.append('Password must contain at least one special character')
    
    if errors:
        raise ValueError(' '.join(errors))
    return value

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class ClientCreate(BaseModel):
    userName: str
    clientFirstName: str
    clientLastName: str
    clientPhoneNumber: str
    clientEmail: str
    selectedPackage :str
    selectedSector :str

    class Config:
        orm_mode = True

class ForgotPasswordRequest(BaseModel):
    user_name: str

class PasswordChangeRequest(BaseModel):
    user_name: str
    current_password: str
    new_password: str


class ResetPasswordRequest(BaseModel):
    user_name: str
    recovery_code: str
    new_password: str


