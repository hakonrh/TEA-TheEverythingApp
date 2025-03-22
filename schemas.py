from pydantic import BaseModel
import datetime

class AccountCreate(BaseModel):
    username: str
    email: str
    password: str