from pydantic import BaseModel

class AccountCreate(BaseModel):
    username: str
    email: str
    password: str

class CreatePostRequest(BaseModel):
    content: str

class EditPostRequest(BaseModel):
    new_content: str