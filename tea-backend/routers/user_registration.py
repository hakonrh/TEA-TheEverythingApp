import schemas
import models
import jwt
from datetime import datetime, timedelta
import pytz

from database import engine, SessionLocal

from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse

from models import Account

from passlib.context import CryptContext

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

SECRET_KEY = "tell_no_one"
ALGORITHM = "HS256"

router = APIRouter()

async def get_session():
    async with SessionLocal() as session:
        yield session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)

# Function for generating JWT
def create_access_token(data: dict, expires_delta: int = 60):
    to_encode = data.copy()
    expire = datetime.now(pytz.utc) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register")
async def register_account(account: schemas.AccountCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Account).where((Account.email == account.email) | (Account.username == account.username)))
    existing_account = result.scalars().first()

    if existing_account:
        if existing_account.email == account.email:
            raise HTTPException(status_code=400, detail="Email already registered")
        if existing_account.username == account.username:
            raise HTTPException(status_code=400, detail="Username already taken")

    encrypted_password = get_hashed_password(account.password)

    new_account = Account(
        username=account.username,
        email=account.email,
        passwordhash=encrypted_password
    )

    session.add(new_account)
    await session.commit()
    await session.refresh(new_account)

    return {"message": "Account created successfully"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/login")
async def login(
    email: str = Form(...), 
    password: str = Form(...), 
    session: AsyncSession = Depends(get_session)
):

    result = await session.execute(select(Account).where(Account.email == email))
    account = result.scalars().first()

    if not account or not verify_password(password, account.passwordhash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": account.email, "id": account.accountid})

    response = JSONResponse(
        content={
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 60 * 60  # Expiration time in seconds
        }
    )
    response.headers["Authorization"] = f"Bearer {access_token}"

    return response
