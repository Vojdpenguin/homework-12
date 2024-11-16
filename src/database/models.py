from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contacts(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    surname = Column(String(30), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    phone_number = Column(String(20), nullable=False)
    birthday = Column(Date)
