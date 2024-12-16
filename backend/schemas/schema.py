from pydantic import BaseModel, EmailStr, Field
from typing import Literal, List, Optional

# Pydantic schemas
class UserSignup(BaseModel):
    username: str
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    role: str

class UserLogin(BaseModel):
    username: str
    password: str

class ConfigurationCreate(BaseModel):
    agent_name: str
    model: str
    temperature: float
    system_message: str
    tools: str
    presence_penalty: float
    frequency_penalty: float
    top_p: float
    max_tokens: int
    agent_url: str

class Token(BaseModel):
    access_token: str
    token_type: str
