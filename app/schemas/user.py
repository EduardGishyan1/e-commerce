import re
from enum import Enum
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.utils.input_validator import check_input_parameter, is_valid_namesurname

class Role(str, Enum):
  admin = "admin"
  vendor = "vendor"
  customer = "customer"

class UserBase(BaseModel):
  username: str = Field(..., json_schema_extra={"description": "The username of the user"})
  name: str = Field(..., json_schema_extra={"description": "The name of the user"})
  surname: str = Field(..., json_schema_extra={"description": "The surname of the user"})
  email: str
  image_url: str = None

  model_config = ConfigDict(from_attributes=True)

  @field_validator('name', mode='before')
  @classmethod
  def validate_name(cls, name: str) -> str:
    if not name:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail="Name can't be empty.")
    name=check_input_parameter(name)
    if not 3 <= len(name) <= 100:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Name should be between 3 and 100 characters in length.")
    if not is_valid_namesurname(name):
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Name should contain theses symbols -, &, _ , ' ")
    return name

  @field_validator('surname', mode='before')
  @classmethod
  def validate_surname(cls, surname: str) -> str:
    if not surname:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail="Surname can't be empty.")
    surname=check_input_parameter(surname)

    if not 1 <= len(surname) <= 100:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Surname should be between 1 and 100 characters in length.")
    if not is_valid_namesurname(surname):
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Name should contain theses symbols -, &, _ , ' ")
    return surname

  @field_validator('username', mode='before')
  @classmethod
  def validate_username(cls, username: str) -> str:
    if not username:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail="Empty username")
    username=check_input_parameter(username)

    if not 3 <= len(username) <= 50:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail="Username should be between 3 and 50 characters in length.")

    return username

class SensitiveInfoBase(BaseModel):
  country: Optional[str] = Field(max_length=50, default=None)
  city: Optional[str] = Field(max_length=50, default=None)
  state: Optional[str] = Field(max_length=50, default=None)
  street: Optional[str] = Field(max_length=50, default=None)
  zip_code: Optional[str] = Field(max_length=50, default=None)

class UserCreate(UserBase):
  password: str = Field(...)
  sensitive_info: Optional[SensitiveInfoBase] = None
  phone_number: str = Field(None, json_schema_extra={"description": "The phone number of the user"})
  # If you want to create admin uncomment below and then comment line below
  role: Role = Field(Role.admin, json_schema_extra={"description": "The role of the user"})

  @field_validator('phone_number', mode='before')
  @classmethod
  def validate_phone_number(cls, phone_number: str) -> str:
    if not re.match(r"^\+\d{6,}$", phone_number):
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid phone number")
    return phone_number

  @field_validator('password', mode='before')
  @classmethod
  def validate_password(cls, password: str) -> str:
    if not re.match(r"^(?=.*?[A-Z])(?=.*?[a-z])"
                    r"(?=.*?[0-9])(?=.*?[#?!@$%^&*-./]).{8,}$", password):

      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Password must be at least 8 characters long and "
               "contain at least one uppercase letter, one lowercase letter, "
               "one number, and one special character.")

    if " " in password:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Password can't contain spaces.")

    return password

  @field_validator('email', mode='before')
  @classmethod
  def validate_email(cls, email: str) -> str:
    email = email.strip().lower()
    if not email:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Email can't be empty.")

    pattern = (r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*"
               r"@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+"
               r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")

    if not re.match(pattern, email):
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid email format.")

    return email

class UserUpdate(BaseModel):
  username: Optional[str] = Field(default=None, json_schema_extra={"description": "The username of the user"})
  name: Optional[str] = Field(default=None, json_schema_extra={"description": "The name of the user"})
  surname: Optional[str] = Field(default=None, json_schema_extra={"description": "The surname of the user"})
  email: Optional[str] = Field(default=None, json_schema_extra={"description": "The email of the user"})
  image_url: Optional[str] = None
  phone_number: Optional[str] = Field(default=None, json_schema_extra={"description": "The phone number of the user"})
  sensitive_info: Optional[SensitiveInfoBase] = None

  @field_validator('name', mode='before')
  @classmethod
  def validate_name(cls, name: str) -> str:
    if not name:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail="Name can't be empty.")
    name=check_input_parameter(name)
    if not 3 <= len(name) <= 100:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Name should be between 3 and 100 characters in length.")
    if not is_valid_namesurname(name):
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Name should contain theses symbols -, &, _ , ' ")
    return name
  
  @field_validator('email', mode='before')
  @classmethod
  def validate_email(cls, email: Optional[str]) -> Optional[str]:
    email = email.strip().lower()
    if not email:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Email can't be empty.")

    pattern = (r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*"
               r"@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+"
               r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")

    if not re.match(pattern, email):
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid email format.")

    return email
  
  @field_validator('surname', mode='before')
  @classmethod
  def validate_surname(cls, surname: str) -> str:
    if not surname:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail="Surname can't be empty.")
    surname=check_input_parameter(surname)

    if not 1 <= len(surname) <= 100:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Surname should be between 1 and 100 characters in length.")
    if not is_valid_namesurname(surname):
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Surname should contain theses symbols -, &, _ , ' ")
    return surname

  @field_validator('username', mode='before')
  @classmethod
  def validate_username(cls, username: str) -> str:
    if not username:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail="Empty username")
    username=check_input_parameter(username)

    if not 3 <= len(username) <= 50:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail="Username should be between 3 and 50 characters in length.")

    return username

class UserResponse(BaseModel):
  id: int
  username: str = Field(..., json_schema_extra={"description": "The username of the user"})
  name: str = Field(..., json_schema_extra={"description": "The name of the user"})
  surname: str = Field(..., json_schema_extra={"description": "The surname of the user"})
  email: str = Field(..., json_schema_extra={"description": "The email of the user"})
  phone_number: str = Field(None, json_schema_extra={"description": "The phone number of the user"})
  image_url: str = None
  sensitive_info: Optional[SensitiveInfoBase] = None

  model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
  access_token: str
  token_type: str

class DefaultUser(BaseModel):
  email: str = Field(..., json_schema_extra={"description": "The email of the user"})

  @field_validator('email', mode='before')
  @classmethod
  def validate_email(cls, email: str) -> str:
    email = email.strip().lower()
    if not email:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Email can't be empty.")

    pattern = (r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*"
               r"@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+"
               r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")

    if not re.match(pattern, email):
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid email format.")

    return email

class UserLogin(DefaultUser):
  password: str = Field(..., min_length=1, json_schema_extra={"description": "The password of the user"})

class ChangePassword(BaseModel):
  password: str
  new_password: str

class PasswordInitiate(BaseModel):
  email: str = Field(..., json_schema_extra={"description": "The email of the user"})

class SetNewPassword(BaseModel):
  email: str = Field(..., json_schema_extra={"description": "The email of the user"})
  new_password: str
  repeat_password: str
  token: str = Field(..., json_schema_extra={"description": "The email of the user"})