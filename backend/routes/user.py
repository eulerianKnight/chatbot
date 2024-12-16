from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from models.user import User
from dependencies import get_db
from schemas.schema import UserSignup, Token, UserLogin

user_router = APIRouter()


@user_router.post("/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    if (
        db.query(User)
        .filter((User.email == user.email) | (User.username == user.username))
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    new_user = User(
        username=user.username,
        first_name=user.firstname,
        last_name=user.lastname,
        email=user.email,
        role=user.role,
    )
    new_user.hash_password(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User has been successfully created."}


@user_router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if user is None or not user.verify_password(user_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials."
        )
    token = user.generate_token()
    return Token(access_token=token, token_type="bearer")
