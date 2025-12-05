# from fastapi import APIRouter, Depends, HTTPException, FastAPI
# from sqlalchemy.orm import Session
# from fastapi.security import OAuth2PasswordBearer
# from datetime import datetime, timedelta, timezone
# from jose import jwt, JWTError
# from passlib.context import CryptContext
#
# from app.database import get_db, engine, base
# from app.models import User, Task
# from app.schemas import UserCreate, Login, TaskCreate
#
# secret_key = "masoom@805"
# algorithm = "HS256"
# access_token_expire_minutes = 60
#
#
#
#
# base.metadata.create_all(engine)
#
# app = FastAPI()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
#
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





from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .models import User

SECRET_KEY = "masoom@805"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=403, detail="Invalid token")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
