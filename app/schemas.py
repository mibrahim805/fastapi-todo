# from pydantic import BaseModel
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






from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

class TaskCreate(BaseModel):
    title: str
    description: str

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    user_id: int

    class Config:
        from_attributes = True

