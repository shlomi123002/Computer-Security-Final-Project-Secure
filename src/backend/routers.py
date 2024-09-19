from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import ClientCreate,UserCreate, UserLogin
from crud import create_user, validate_user, get_user_by_name, update_password,create_client,get_user_by_email
from database import get_db
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
    user_email: str

class ResetPasswordRequest(BaseModel):
    user_email: str
    recovery_code: int
    new_password: str

top_recovery_code = 0

@user_router.post("/forgot-password/")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    global top_recovery_code
    user = get_user_by_email(db, request.user_email) 
    if not user:
        raise HTTPException(status_code=404, detail="User ID not found")
    
    # Generate and send the recovery code
    recovery_code = send_recovery_code(user.email)
    
    # Store the recovery code in the user object or databaseS
    top_recovery_code = recovery_code
    db.commit()
    
    return {"msg": "Recovery code sent to your email"}

@user_router.post("/reset-password/")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.user_email)  # Change to use user_id
    if not user:
        raise HTTPException(status_code=404, detail="User ID not found")
    
    # Check if the provided recovery code matches the one stored
    if int(top_recovery_code) != request.recovery_code:
        raise HTTPException(status_code=400, detail="Invalid recovery code")
    
    # Update the password
    update_password(db, user, request.new_password)
    return {"msg": "Password reset successful"}

class PasswordChangeRequest(BaseModel):
    user_name: str
    current_password: str
    new_password: str

# Password change route
@user_router.put("/change-password/") 
async def change_password(request: PasswordChangeRequest, db: Session = Depends(get_db)):
    user = get_user_by_name(db, request.user_name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Step 1: Verify current password
    if not verify_password(request.current_password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect current password")

    # Step 2: Hash the new password and update the database
    hashed_new_password = request.new_password
    user.password = hashed_new_password
    db.commit()

    return {"msg": "Password updated successfully"}

#add a client to the clients table
@user_router.post("/Dashboard/")
def add_client(client: ClientCreate, db: Session = Depends(get_db)):
    try:
        new_client = create_client(db, client)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"msg": "Client added successfully", "client": new_client}