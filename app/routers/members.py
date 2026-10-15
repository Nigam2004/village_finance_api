from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.member import Member
from app.schemas.member import MemberCreate, MemberUpdate, MemberOut

router = APIRouter(prefix="/api/members", tags=["Members"])


@router.post("", response_model=MemberOut, status_code=status.HTTP_201_CREATED)
def create_member(payload: MemberCreate, db: Session = Depends(get_db)):
    member = Member(**payload.model_dump())
    db.add(member)
    db.flush()
    member.member_acc=f"MDR{member.id:04d}"
    db.commit()
    db.refresh(member)
    return member


@router.get("", response_model=list[MemberOut])
def list_members(skip: int = 0, limit: int = 100, search: str | None = None, db: Session = Depends(get_db)):
    stmt = select(Member).order_by(Member.id.desc()).offset(skip).limit(min(limit, 500))
    if search:
        stmt = stmt.where(Member.name.ilike(f"%{search}%"))
    return db.scalars(stmt).all()


@router.get("/{member_id}", response_model=MemberOut)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member=db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.patch("/{member_id}", response_model=MemberOut)
def update_member(member_id: str, payload: MemberUpdate, db: Session = Depends(get_db)):
    member=db.query(Member).filter(Member.member_id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(member, key, value)
    db.commit()
    db.refresh(member)
    return member


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: str, db: Session = Depends(get_db)):
    member=db.query(Member).filter(Member.member_id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    if member.loans or member.transactions:
        raise HTTPException(status_code=409, detail="Member has financial records; archive them instead of deleting.")
    db.delete(member)
    db.commit()
    return{"rsp":"member deletedsucces"}
