from pydantic import BaseModel, Field
from typing import Annotated, Optional
from db_setup import SessionLocal, Base
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy import Column, Integer, String, Float, Date, Uuid, Boolean, ForeignKey, text

#create pydantic models
class CategoryBase(BaseModel):
    category: str
    income_cat: bool
    username: str
    category_id: Optional[UUID] = None

class RecordBase(BaseModel):
    record_id: Optional[UUID] = None
    date: Optional[str] = None
    category_id: UUID
    description: Optional[str] = None
    amount: float
    #username: str

class GoalBase(BaseModel):
    title: str
    amount: float
    priority: int = Field(ge=1, le=5, default=1)
    username: str
    goal_id: Optional[UUID] = None

class UserBase(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str

#create database session and dependency

def get_db():
    db = SessionLocal()
    db.execute(text('pragma foreign_keys=ON'))
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

#create models of SQL tables
class Categories(Base):
    __tablename__ = 'categories'

    category = Column(String(100))
    income_cat = Column(Boolean)
    username = Column(String(25), ForeignKey('users.username', onupdate='CASCADE', ondelete='CASCADE'))
    category_id = Column(Uuid, primary_key=True, index=True)

class Records(Base):
    __tablename__ = 'records'

    date = Column(Date)
    category_id = Column(Uuid, ForeignKey('categories.category_id', onupdate='CASCADE', ondelete='CASCADE'))
    description = Column(String(150))
    amount = Column(Float)
    #username = Column(String(25), ForeignKey('users.username', onupdate='CASCADE', ondelete='CASCADE'))
    record_id = Column(Uuid, primary_key=True, index=True)

class Goals(Base):
    __tablename__ = 'savings_goals'

    title = Column(String(100), primary_key=True, index=True)
    amount = Column(Float)
    priority = Column(Integer)
    username = Column(String(25), ForeignKey('users.username', onupdate='CASCADE', ondelete='CASCADE'))
    goal_id = Column(Uuid, primary_key=True, index=True)

class Users(Base):
    __tablename__ = 'users'

    username = Column(String(25), primary_key=True, index=True)
    password = Column(String(25))
    first_name = Column(String(30))
    last_name = Column(String(30))
    