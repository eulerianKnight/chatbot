import time
import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from config import get_settings
from models.user import User

# Constants
SECRET_KEY = f"{get_settings().SECRET_KEY}"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def decode_jwt(token: str) -> dict:
    decoded_token = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
    return decoded_token if decoded_token["exp"] >= time.time() else None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request=request)
        if credentials:
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid Token or Expired Token.",
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid Authorization code.",
            )

    def verify_jwt(self, jwt_token: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decode_jwt(jwt_token)
        except Exception as e:
            payload = None

        if payload:
            isTokenValid = True
        return isTokenValid
