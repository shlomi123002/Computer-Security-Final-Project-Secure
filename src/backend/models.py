from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    userID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    userName = Column(String(200), unique=True, index=True, nullable=False)
    email = Column(String(200), unique=False, index=True, nullable=False)
    password = Column(String(200), nullable=False)
    salt = Column(String(200), nullable=True)

class Client(Base):
    __tablename__ = "clients"
    userName = Column(String(200), primary_key=True, index=True, nullable=False)
    clientFirstName = Column(String(200), index=True, nullable=False)
    clientLastName = Column(String(200), index=True, nullable=False)
    clientEmail = Column(String(200), index=True, nullable=False)
    clientPhoneNumber = Column(String(200), index=True, nullable=False)

   
