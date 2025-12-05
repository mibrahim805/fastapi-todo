# from fastapi import FastAPI
# from app.database import engine, Base
# from app.auth import router as auth_router
# from app.tasks import router as tasks_router

# app = FastAPI()

# Create database tables
# Base.metadata.create_all(bind=engine)

# Include all routes
# app.include_router(auth_router, prefix="/auth", tags=["Auth"])
# app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])


# @app.get("/")
# def root():
#     return {"message": "API is running!"}












# from fastapi import FastAPI, HTTPException, Depends
# from fastapi.security import OAuth2PasswordBearer
# from pydantic import BaseModel
# from passlib.context import CryptContext
# from jose import jwt, JWTError
# from datetime import datetime, timedelta, timezone
# from typing import List, Generator
# from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine
# from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
# from sqlalchemy.sql.sqltypes import Boolean
#
#
# secret_key = "masoom@805"
# algorithm = "HS256"
# access_token_expire_minutes = 60
# database_url = "mysql+pymysql://ibrahim:123@127.0.0.1/Todo_list"
#
# engine = create_engine(database_url)
# session = sessionmaker(bind=engine)
# base = declarative_base()
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
#
# base.metadata.create_all(engine)
#
# app = FastAPI()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# def get_db() -> Generator[Session, None, None]:
#     db = session()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)
#
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)
#
# def create_access_token(data: dict) -> str:
#     to_encode = data.copy()
#     expire = datetime.now(timezone.utc) + timedelta(minutes=access_token_expire_minutes)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
#     return encoded_jwt
#
# def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, secret_key, algorithms=[algorithm])
#         email: str = payload.get("sub")
#         user_id: int = payload.get("user_id")
#         if not email or not user_id:
#             raise HTTPException(status_code=403, detail="Invalid token")
#         user = db.query(User).filter(User.id == user_id).first()
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         return user
#     except JWTError:
#         raise HTTPException(status_code=403, detail="Invalid token")
#
#
# class UserCreate(BaseModel):
#     name: str
#     email: str
#     password: str
#
# class Login(BaseModel):
#     email: str
#     password: str
#
# class TaskCreate(BaseModel):
#     title: str
#     description: str
#
# class TaskOut(BaseModel):
#     title: str
#     description: str
#     completed: bool
#     user_id: int
#     id: int
#     class Config:
#         from_attributes = True
#
#
# @app.post("/signup", status_code=201)
# def signup(user: UserCreate, db: Session = Depends(get_db)):
#     exists = db.query(User).filter(User.email == user.email).first()
#     if exists:
#         raise HTTPException(status_code=400, detail="Email already exists")
#     new_user = User(email=user.email, password=hash_password(user.password))
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return {"message": "User created successfully"}
#
#
# @app.post("/login")
# def login(login_data: Login, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == login_data.email).first()
#     if not user:
#         raise HTTPException(status_code=400, detail="Incorrect email or password")
#     if not verify_password(login_data.password, user.password):
#         raise HTTPException(status_code=400, detail="Incorrect email or password")
#     access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
#     return {"access_token": access_token, "token_type": "bearer"}
#
# @app.post("/tasks", status_code=201)
# def add_task(task: TaskCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     new_task = Task(title = task.title, description = task.description, user_id = user.id, completed = False )
#     db.add(new_task)
#     db.commit()
#     db.refresh(new_task)
#     return { "message": "Task added successfully"}
#
#
# @app.get("/tasks")
# def get_tasks(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     tasks = db.query(Task).filter(Task.user_id == user.id).all()
#     if not tasks:
#         raise HTTPException(status_code=404, detail="No tasks found")
#     return tasks
#
# @app.get("/tasks/{task_id}", status_code=201)
# def get_task(task_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
#     if not task:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return task
#
#
# @app.put("/tasks/{task_id}/complete")
# def complete_task(task_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
#     if not task:
#         raise HTTPException(status_code=404, detail="Task not found")
#     task.completed = True
#     db.commit()
#     return {"message": "Task completed successfully"}
#
#
# @app.delete("/tasks/{task_id}")
# def delete_task(task_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
#     if not task:
#         raise HTTPException(status_code=404, detail="Task not found")
#     db.delete(task)
#     db.commit()
#     return {"message": "Task deleted successfully"}







from fastapi import FastAPI
from .routers import users, tasks
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(tasks.router)
