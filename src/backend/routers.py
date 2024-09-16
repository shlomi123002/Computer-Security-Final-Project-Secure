from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import UserCreate, UserLogin
from crud import create_user
from database import get_db
from crud import create_user, validate_user
from crud import get_user_by_email, update_password
from utils import send_recovery_code, verify_password
from pydantic import BaseModel

user_router = APIRouter()

@user_router.post("/register/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        result = create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result

@user_router.post("/login/")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    try:
        validated_user = validate_user(db, user.username, user.password)
        if validated_user:
            return {"message": "Login successful"}
        else:
            raise HTTPException(status_code=400, detail="Invalid username or password")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
 
class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    email: str
    recovery_code: str
    new_password: str

@user_router.post("/forgot-password/")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    
    # Generate and send the recovery code
    recovery_code = send_recovery_code(user.email)
    
    # Store the recovery code in the user object or database (you may want to implement a better storage mechanism)
    user.recovery_code = recovery_code
    db.commit()
    
    return {"msg": "Recovery code sent to your email"}

@user_router.post("/reset-password/")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    
    # Check if the provided recovery code matches the one stored
    if user.recovery_code != request.recovery_code:
        raise HTTPException(status_code=400, detail="Invalid recovery code")
    
    # Update the password
    update_password(db, user, request.new_password)
    return {"msg": "Password reset successful"}