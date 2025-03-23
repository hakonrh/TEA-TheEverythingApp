import schemas
import models
from database import engine, SessionLocal
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from models import Account
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
router = APIRouter()

async def get_session():
    async with SessionLocal() as session:
        yield session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)

@router.post("/register")
async def register_account(account: schemas.AccountCreate, session: AsyncSession = Depends(get_session)):
    # Check if the email already exists
    result = await session.execute(select(Account).where(Account.email == account.email))
    existing_account = result.scalars().first()

    if existing_account:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    encrypted_password = get_hashed_password(account.password)

    # Create a new account object
    new_account = Account(
        username=account.username,
        email=account.email,
        passwordhash=encrypted_password
    )

    session.add(new_account)
    await session.commit()
    await session.refresh(new_account)

    return {"message": "Account created successfully"}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/login")
async def login(
    email: str = Form(...), 
    password: str = Form(...), 
    session: AsyncSession = Depends(get_session)
):
    # Fetch the account using ORM
    result = await session.execute(select(Account).where(Account.email == email))
    account = result.scalars().first()

    if not account or not verify_password(password, account.passwordhash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful"}