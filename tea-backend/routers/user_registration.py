import schemas
import models
from database import engine, SessionLocal
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from models import Account, Base
from passlib.context import CryptContext
from sqlalchemy.orm import Session

router = APIRouter()

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)

@router.post("/register")
def register_account(account: schemas.AccountCreate, session: Session = Depends(get_session)):
    existing_account = session.query(models.Account).filter_by(email=account.email).first()
    if existing_account:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password =get_hashed_password(account.password)

    new_account = models.Account(username=account.username, email=account.email, password=encrypted_password )

    session.add(new_account)
    session.commit()
    session.refresh(new_account)

    return {"message":"account created successfully"}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/login")
def login(
    email: str = Form(...), 
    password: str = Form(...), 
    session: Session = Depends(get_session)
):
    account = session.query(models.Account).filter_by(Email=email).first()

    if not account or not verify_password(password, account.PasswordHash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful"}