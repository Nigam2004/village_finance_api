from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.admin import Admin
from app.schemas.admin import AdminLogin, AdminOut, AdminRegister, TokenOut
from app.security import (
    create_access_token,
    get_current_admin,
    hash_password,
    verify_password,
)

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.post("/register", response_model=AdminOut, status_code=status.HTTP_201_CREATED)
def register_admin(payload: AdminRegister, db: Session = Depends(get_db)):
    email = str(payload.email).strip().lower()
    existing_admin = db.scalar(select(Admin).where(Admin.email == email))
    if existing_admin is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )

    admin = Admin(
        full_name=payload.full_name,
        email=email,
        password_hash=hash_password(payload.password),
    )
    db.add(admin)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        ) from None

    db.refresh(admin)
    return admin


@router.post("/login", response_model=TokenOut)
def login_admin(payload: AdminLogin, db: Session = Depends(get_db)):
    email = str(payload.email).strip().lower()
    admin = db.scalar(select(Admin).where(Admin.email == email))
    if admin is None or not verify_password(payload.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenOut(access_token=create_access_token(admin.id))


@router.get("/me", response_model=AdminOut)
def get_admin_profile(admin: Admin = Depends(get_current_admin)):
    return admin
