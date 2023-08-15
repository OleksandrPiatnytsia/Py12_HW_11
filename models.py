from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    sur_name = Column(String(100))
    email = Column(String(120))
    phone = Column(String(13))
    birthday = Column(DateTime)



