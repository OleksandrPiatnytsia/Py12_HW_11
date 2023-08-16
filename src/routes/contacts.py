from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter
from sqlalchemy.orm import Session

from pydantic import EmailStr

from src.database.db import get_db
from src.schemas import ContactSchema

import src.repository.contacts as res_contacts

router = APIRouter(prefix='/api/contacts', tags=["contacts"])
birthday_router = APIRouter(prefix='/api/week_birthday', tags=["birthday"])


@router.get("/", response_model=List[ContactSchema])
def get_contacts(session: Session = Depends(get_db)):
    return res_contacts.get_contacts(session)


@router.get("/{contact_id}", response_model=ContactSchema)
def get_contact_by_id(contact_id: int = Path(ge=1), session: Session = Depends(get_db)):
    contact = res_contacts.get_contact_by_id(contact_id=contact_id, session=session)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact


@router.get("/name/{name}", response_model=ContactSchema)
def get_contact_by_name(name: str = Path(min_length=3, max_length=100), session: Session = Depends(get_db)):
    contact = res_contacts.get_contact_by_name(name=name, session=session)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact


@router.get("/email/{email}", response_model=ContactSchema)
def get_contact_by_email(email: EmailStr, session: Session = Depends(get_db)):
    contact = res_contacts.get_contact_by_email(email=email, session=session)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact


@router.get("/sur_name/{sur_name}", response_model=ContactSchema)
def get_contact_by_sur_name(sur_name: str = Path(min_length=3, max_length=100), session: Session = Depends(get_db)):
    contact = res_contacts.get_contact_by_sur_name(sur_name=sur_name, session=session)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact


@router.post("/", response_model=ContactSchema, status_code=status.HTTP_201_CREATED)
def create_contact(body: ContactSchema, session: Session = Depends(get_db)):
    if res_contacts.get_contact_by_phone(phone=body.phone, session=session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Phone {body.phone} already exist!"
        )

    return res_contacts.create_contact(body=body, session=session)


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int = Path(ge=1), session: Session = Depends(get_db)):
    contact = res_contacts.get_contact_by_id(contact_id=contact_id, session=session)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )

    return res_contacts.delete_contact(contact=contact, session=session)


@router.patch("/{contact_id}", response_model=ContactSchema)
def update_contact(body: ContactSchema, contact_id: int = Path(ge=1), session: Session = Depends(get_db)):
    contact = res_contacts.get_contact_by_id(contact_id=contact_id, session=session)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )

    contact_phone = res_contacts.get_contact_by_phone(phone=body.phone, session=session)

    if contact_phone and contact.id != contact_phone.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Another contact id={contact_phone.id} already had phone {body.phone}!"
        )

    return res_contacts.update_contact(body=body, contact=contact, session=session)


@birthday_router.get("/a", response_model=List[ContactSchema])
def get_contact_week_birthdays(session: Session = Depends(get_db)):
    return res_contacts.get_contact_week_birthdays(session=session)
