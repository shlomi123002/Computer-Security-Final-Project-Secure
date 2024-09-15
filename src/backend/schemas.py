from pydantic import BaseModel, EmailStr, validator
import re
import json
from pathlib import Path
import os


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


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

class UserLogin(BaseModel):
    username: str
    password: str
