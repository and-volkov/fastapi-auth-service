from typing import List, Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class Service(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ServiceCreate(BaseModel):
    name: str


class ServiceList(BaseModel):
    services: List[Service]

    class Config:
        from_attributes = True


class Role(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class RoleCreate(BaseModel):
    name: str


class RoleList(BaseModel):
    roles: List[Role]

    class Config:
        from_attributes = True


class UserServiceRole(BaseModel):
    id: int
    user_id: int
    role_id: int
    service_id: int

    class Config:
        from_attributes = True


class UserServiceRoleCreate(BaseModel):
    user_id: int
    role_id: int
    service_id: int


class UserServiceRoleList(BaseModel):
    user_service_roles: List[UserServiceRole]

    class Config:
        from_attributes = True


class UserServiceRoleDelete(BaseModel):
    user_id: Optional[int]
    service_id: Optional[int]


class UserServiceRoleResponse(BaseModel):
    role_id: int
    service_id: int


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    is_superuser: bool = False

    class Config:
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
    service_roles: List[UserServiceRoleResponse]

    class Config:
        from_attributes = True


class UserList(BaseModel):
    users: List[UserResponse]

    class Config:
        from_attributes = True


class UserCreateResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class UserUpdateResponse(BaseModel):
    user: UserUpdate

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    users: List[User]

    class Config:
        from_attributes = True
