# from typing import Generator
#
# from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine
# from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
#
#
# database_url = "mysql+pymysql://ibrahim:123@127.0.0.1/Todo_list"
#
# engine = create_engine(database_url)
# session = sessionmaker(bind=engine)
# base = declarative_base()
#
# def get_db() -> Generator[Session, None, None]:
#     db = session()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# # class Base:
# #     metadata = None




from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

database_url = "mysql+pymysql://ibrahim:123@127.0.0.1/Todo_list"

engine = create_engine(database_url)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
