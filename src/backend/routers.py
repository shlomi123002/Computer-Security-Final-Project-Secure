from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import ClientCreate,UserCreate, UserLogin
from crud import create_user, validate_user, update_password,create_client, verify_password, insert_into_passwordhistory_table, generate_salt, number_of_password_history
from database import get_db
from utils import send_recovery_code, get_password_hash
from pydantic import BaseModel
from sqlalchemy import text


user_router = APIRouter()

@user_router.post("/register/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        result = create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result

# sql injection for login page -> admin' OR 1=1 #
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
    user_name: str

recovery_code = 0

@user_router.post("/forgot-password/")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    
    get_email_query = text(f"SELECT email FROM users WHERE userName = '{request.user_name}' LIMIT 1;")
    email = db.execute(get_email_query).fetchone()

    if not email :
        raise ValueError("Username not found")
    
    global recovery_code
    # Generate and send the recovery code
    recovery_code = send_recovery_code(email[0])
    
    return {"msg": "Recovery code sent to your email"}

class ResetPasswordRequest(BaseModel):
    user_name: str
    recovery_code: int
    new_password: str

@user_router.post("/reset-password/")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    
    # Check if the provided recovery code matches the one stored
    if int(recovery_code) != request.recovery_code:
        raise HTTPException(status_code=400, detail="Invalid recovery code")
    
    # Update the password
    update_password(db, request.user_name, request.new_password)
    return {"msg": "Password reset successful"}

class PasswordChangeRequest(BaseModel):
    user_name: str
    current_password: str
    new_password: str

@user_router.put("/change-password/") 
def change_password(user: PasswordChangeRequest, db: Session = Depends(get_db)):
    
    # Verify current password
    if not verify_password(db, user.current_password, user.user_name):
        raise HTTPException(status_code=400, detail="Incorrect current password")
    
    number_of_history = number_of_password_history()

    if not update_password(db, user.user_name, user.new_password) :
         raise HTTPException(status_code=400, detail=f"The new password cannot be one of the last '{number_of_history}' used passwords.")
    
    return {"msg": "Password updated successfully"}

#add a client to the clients table
@user_router.post("/Dashboard/")
def add_client(client: ClientCreate, db: Session = Depends(get_db)):
    try:
        create_client(db, client)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"msg": "Client added successfully"}

@user_router.get("/client-table")
def get_clients(db: Session = Depends(get_db)):
    try:
        # Raw SQL query to fetch all clients
        query = text("SELECT * FROM clients")

        # Execute the query
        result = db.execute(query)

        # Fetch all rows from the result
        clients = result.fetchall()  # Use fetchall() to get all results

        # If no clients are found, raise an HTTPException
        if not clients:
            raise HTTPException(status_code=404, detail="No clients found")
        
        # Convert the rows to a list of dictionaries
        client_list = []
        for row in clients:
            clientID = row["clientID"]
            print("client id :" ,clientID)
            package_query = text(f"SELECT * FROM internet_packages WHERE client_id = '{clientID}';")
            packages = db.execute(package_query)

            for package_info in packages :
                package_information = package_info["name"] + " ,speed:" + package_info["speed"] + ", Data Limit:" + package_info["data_limit"] + ", price:" + package_info["price"]
                sector_query = text(f"SELECT name FROM sectors WHERE client_id = '{clientID}';")
                sector = db.execute(sector_query).fetchone()
                
                client_list.append({
                "clientFirstName": row["clientFirstName"],
                "clientLastName": row["clientLastName"],
                "clientEmail": row["clientEmail"],
                "clientPhoneNumber": row["clientPhoneNumber"],
                "selectedPackage":  package_information ,
                "selectedSector" : sector["name"]
            })
            
            

        return client_list
    
    except Exception as e:
        # Log the error and raise a generic HTTP exception
        raise HTTPException(status_code=500, detail="Internal Server Error")
