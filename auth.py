from fastapi import APIRouter,Depends,HTTPException,status
from database import get_db,db_dependency
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
import jwt
from models import User
from schemas import UserCreate,UserLogin
from auth_service import hash_password,verify_password,create_access_token,SECRET_KEY, ALGORITHM


bearer_scheme = HTTPBearer()

def get_current_user(
    db:db_dependency,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
       
):
    token=credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id = int(user_id)

    except (InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
    

router =APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/register",status_code=status.HTTP_201_CREATED,)
async def register_user(user_data:UserCreate,db:db_dependency):
    existing_user=(db.query(User).filter(User.email==user_data.email).first())
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered"
        )

    new_user=User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "email": new_user.email,
    }


@router.post("/login")
async def login_user(user_data:UserLogin,db:db_dependency):
    user=(db.query(User).filter(User.email==user_data.email).first())

    if user is None or not verify_password(user_data.password,user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token=create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {
        "user_id": current_user.id,
        "email": current_user.email,
    }