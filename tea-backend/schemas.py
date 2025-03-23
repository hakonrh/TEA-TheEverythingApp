from pydantic import BaseModel

class AccountCreate(BaseModel):
    username: str
    email: str
    password: str

class CreatePostRequest(BaseModel):
    accountid: int
    content: str

class EditPostRequest(BaseModel):
    accountid: int
    new_content: str

class DeletePostRequest(BaseModel):
    accountid: int