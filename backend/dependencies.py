import jwt
from database import SessionLocal

from fastapi import Depends, HTTPException, status
from services.auth_services import JWTBearer
from models.user import User
from config import get_settings

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(JWTBearer())) -> User:
    try:
        payload = jwt.decode(jwt=token, key=f'{get_settings().SECRET_KEY}', algorithms=['HS256'])
        user_id = payload.get('sub')
        db = SessionLocal()
        return db.query(User).filter(User.id == user_id).first()
    except(jwt.PyJWTError, AttributeError):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)