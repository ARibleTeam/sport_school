from pydantic import BaseModel, EmailStr, validator

class UserSchema(BaseModel):
    id: int
    name: str
    isAdmin: bool
    isAthlete: bool

    class Config:
        from_attributes = True

class SignInRequest(BaseModel):
    email: str
    password: str

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone_number: str

    @validator("password")
    def password_length(cls, password):
        if len(password) > 72:
            raise ValueError("Password must be less than 72 characters")
        return password
