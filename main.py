import os
import pathlib
import time
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status, Path, Query, Request, File, UploadFile
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
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


@app.get("/contacts", response_model=List[ContactSchema], tags=["contacts"])
def get_owners(db: Session = Depends(get_db)):
    contacts = db.query(Contact).all()
    return contacts


@app.get("/contacts/{contact_id}", response_model=ContactSchema, tags=["contacts"])
async def get_owner(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact


@app.post("/contacts", response_model=ContactSchema, tags=["contacts"])
async def create_owner(body: ContactSchema, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(phone=body.phone).first()
    if contact:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail = f"Phone {body.phone} already exist!",
        )
    contact = Contact()
    contact.phone = body.phone
    contact.email = body.email
    contact.name = body.name
    contact.sur_name = body.sur_name
    contact.birthday = body.birthday
    db.add(contact)
    db.commit()
    return contact
