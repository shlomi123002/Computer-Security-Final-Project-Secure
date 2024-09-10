from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    userID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    userName = Column(String(200), unique=True, index=True, nullable=False)
    email = Column(String(200), unique=True, index=True, nullable=False)
    password = Column(String(200), nullable=False)
