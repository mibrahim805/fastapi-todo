# from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
# from sqlalchemy.orm import relationship
# from app.schemas import Base, base
#
#
# class User(base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String(255), unique=True, index=True)
#     password = Column(String(255), nullable=False)
#     tasks = relationship("Task", back_populates="user")
#
# class Task(base):
#     __tablename__ = "tasks"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(255), nullable=False)
#     description = Column(Text)
#     completed = Column(Boolean, default=False)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     user = relationship("User", back_populates="tasks")




from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255), nullable=False)
    tasks = relationship("Task", back_populates="user")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="tasks")
