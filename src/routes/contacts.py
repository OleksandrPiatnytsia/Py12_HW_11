from datetime import datetime
from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter
from sqlalchemy.orm import Session

from pydantic import EmailStr
from sqlalchemy import text

from src.database.db import get_db
from src.schemas import ContactSchema

from src.database.models import Contact

router = APIRouter(prefix='/api/contacts', tags=["contacts"])
birthday_router = APIRouter(prefix='/api/week_birthday', tags=["birthday"])


@router.get("/", response_model=List[ContactSchema])
def get_contacts(session: Session = Depends(get_db)):
    contacts = session.query(Contact).all()
    return contacts


@router.get("/{contact_id}", response_model=ContactSchema)
def get_contact_by_id(contact_id: int = Path(ge=1), session: Session = Depends(get_db)):
    contact = session.query(Contact).filter_by(id=contact_id).first()
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact


@router.get("/name/{name}", response_model=ContactSchema)
def get_contact_by_name(name: str = Path(min_length=3, max_length=100), session: Session = Depends(get_db)):
    contact = session.query(Contact).filter_by(name=name).first()
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact


@router.get("/email/{email}", response_model=ContactSchema)
def get_contact_by_email(email: EmailStr, session: Session = Depends(get_db)):
    contact = session.query(Contact).filter_by(email=email).first()
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact


@router.get("/sur_name/{sur_name}", response_model=ContactSchema)
def get_contact_by_sur_name(sur_name: str = Path(min_length=3, max_length=100), session: Session = Depends(get_db)):
    contact = session.query(Contact).filter_by(sur_name=sur_name).first()
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact


@router.post("/", response_model=ContactSchema, status_code=status.HTTP_201_CREATED)
def create_contact(body: ContactSchema, session: Session = Depends(get_db)):
    contact = session.query(Contact).filter_by(phone=body.phone).first()
    if contact:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Phone {body.phone} already exist!"
        )
    contact = Contact()
    contact.phone = body.phone
    contact.email = body.email
    contact.name = body.name
    contact.sur_name = body.sur_name
    contact.birthday = body.birthday
    session.add(contact)
    session.commit()
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int = Path(ge=1), session: Session = Depends(get_db)):
    contact = session.query(Contact).filter_by(id=contact_id).first()
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    session.delete(contact)
    session.commit()
    return contact


@router.patch("/{contact_id}", response_model=ContactSchema)
def update_contact(body: ContactSchema, contact_id: int = Path(ge=1), session: Session = Depends(get_db)):
    contact = session.query(Contact).filter_by(id=contact_id).first()
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    contact_phone = session.query(Contact).filter_by(phone=body.phone).first()

    if contact_phone and contact.id != contact_phone.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Another contact id={contact_phone.id} already had phone {body.phone}!"
        )

    contact.phone = body.phone
    contact.email = body.email
    contact.name = body.name
    contact.sur_name = body.sur_name
    contact.birthday = body.birthday
    session.add(contact)
    session.commit()
    return contact


@birthday_router.get("/a", response_model=List[ContactSchema])
def get_contact_week_birthdays(session: Session = Depends(get_db)):
    current_date = datetime.now()
    current_month = current_date.month

    contacts = session.execute(text("""
            SELECT *
            FROM contacts AS con
            WHERE EXTRACT(WEEK FROM con.birthday) = EXTRACT(WEEK FROM :current_date)
              AND EXTRACT(MONTH FROM con.birthday) = :current_month;
            """), {"current_date": current_date, "current_month": current_month}).all()

    return contacts
