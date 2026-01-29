from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    get_password_hash,
    get_token_expiry,
    verify_password,
)
from app.database import get_db
from app.dependencies import CurrentUser
from app.models import User
from app.schemas.auth import (
    LoginResponse,
    LogoutResponse,
    RegisterResponse,
    UserLogin,
    UserRegister,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserRegister,
    db: Annotated[Session, Depends(get_db)],
) -> RegisterResponse:
    """
    Register a new user.

    Creates a new user account and returns a JWT token for immediate authentication.
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "VALIDATION_ERROR",
                "message": "Email already registered",
                "details": {"field": "email", "issue": "Email is already in use"},
            },
        )

    # Create new user
    user = User(
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        name=user_data.name,
        timezone=user_data.timezone,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate token
    token = create_access_token(data={"sub": str(user.id)})

    return RegisterResponse(
        user_id=user.id,
        email=user.email,
        name=user.name,
        token=token,
    )


@router.post("/login", response_model=LoginResponse)
def login(
    credentials: UserLogin,
    db: Annotated[Session, Depends(get_db)],
) -> LoginResponse:
    """
    Login with email and password.

    Returns a JWT token for authentication.
    """
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "UNAUTHORIZED",
                "message": "Invalid email or password",
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(data={"sub": str(user.id)})
    expires_at = get_token_expiry()

    return LoginResponse(
        user_id=user.id,
        token=token,
        expires_at=expires_at,
    )


@router.post("/logout", response_model=LogoutResponse)
def logout(current_user: CurrentUser) -> LogoutResponse:
    """
    Logout the current user.

    Note: With stateless JWT tokens, this endpoint primarily serves as
    a signal to the client to discard the token. For true token invalidation,
    implement a token blacklist or use short-lived tokens with refresh tokens.
    """
    return LogoutResponse(message="Logged out successfully")
