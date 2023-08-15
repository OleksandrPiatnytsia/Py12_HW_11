import os
import pathlib
import time
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status, Path, Query, Request, File, UploadFile
from sqlalchemy import text
from sqlalchemy.orm import Session

from db import get_db
from models import Contact
from schemas import OwnerModel, OwnerResponse, CatModel, CatResponse, CatVaccinatedModel

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