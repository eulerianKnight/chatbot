from sqlalchemy import Column, Integer, String, DateTime, Enum
import enum
from datetime import datetime, timedelta
import bcrypt
import jwt

from database import Base
from config import get_settings


class UserRole(enum.Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    first_name = Column(String(50), unique=False, index=True)
    last_name = Column(String(50), unique=False, index=True)
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255))
    role = Column(Enum("admin", "user", name="user_roles"), default="user")
    created_at = Column(DateTime, default=datetime.now)

    def hash_password(self, password: str):
        self.password_hash = bcrypt.hashpw(
            password=password.encode("utf-8"), 
            salt=bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, password: str):
        return bcrypt.checkpw(
            password=password.encode("utf-8"),
            hashed_password=self.password_hash.encode("utf-8"),
        )

    def generate_token(self):
        expiration = datetime.now() + timedelta(hours=1)
        payload = {"sub": str(self.id), "exp": expiration}
        return jwt.encode(
            payload=payload, key=f"{get_settings().SECRET_KEY}", algorithm="HS256"
        )
