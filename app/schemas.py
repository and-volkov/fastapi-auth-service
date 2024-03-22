from typing import List, Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    is_superuser: bool = False

    class Config:
        orm_mode = True
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_superuser: bool

    class Config:
        orm_mode = True


class UserList(BaseModel):
    users: List[UserResponse]

    class Config:
        orm_mode = True


class UserCreateResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True


class UserUpdateResponse(BaseModel):
    user: UserUpdate

    class Config:
        orm_mode = True


class UserListResponse(BaseModel):
    users: List[User]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
