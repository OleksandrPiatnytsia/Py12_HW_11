import os
import pathlib
import time
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status, Path, Query, Request, File, UploadFile
from pydantic import EmailStr, Field
from sqlalchemy import text
from sqlalchemy.orm import Session

from db import get_db
from models import Contact
from schemas import ContactSchema

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Application started"}


@app.get("/api/healthchecker")
def healthchecker(session: Session = Depends(get_db)):
    try:
        # Make request
        result = session.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


@app.get("/api/contacts", response_model=List[ContactSchema], tags=["contacts"])
def get_contacts(session: Session = Depends(get_db)):
    contacts = session.query(Contact).all()
    return contacts


@app.get("/api/contacts/{contact_id}", response_model=ContactSchema, tags=["contacts"])
def get_contact_by_id(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact


@app.get("/api/contacts/name/{name}", response_model=ContactSchema, tags=["contacts"])
def get_contact_by_name(name: str = Path(min_length=3, max_length=100), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(name=name).first()
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact


@app.get("/api/contacts/email/{email}", response_model=ContactSchema, tags=["contacts"])
def get_contact_by_email(email: EmailStr, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(email=email).first()
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact

@app.get("/api/contacts/sur_name/{sur_name}", response_model=ContactSchema, tags=["contacts"])
def get_contact_by_email(sur_name: str = Path(min_length=3, max_length=100), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(sur_name=sur_name).first()
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact


@app.post("/api/contacts", response_model=ContactSchema, tags=["contacts"], status_code=status.HTTP_201_CREATED)
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


@app.delete("/api/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["contacts"])
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


@app.patch("/api/contacts/{contact_id}", response_model=ContactSchema, tags=["contacts"])
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
