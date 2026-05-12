from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import (
    Alumni,
    AlumniCreate,
    AlumniRead,
    AlumniStatus,
    CheckResult,
    ExternalCheckResponse,
    VerifyRequest,
)
from routers.external import check_alumni

router = APIRouter()


@router.post("", response_model=AlumniRead, status_code=201)
def register_alumni(payload: AlumniCreate, session: Session = Depends(get_session)):
    alumni = Alumni.model_validate(payload)
    session.add(alumni)
    session.commit()
    session.refresh(alumni)
    return alumni


@router.get("", response_model=list[AlumniRead])
def list_alumni(session: Session = Depends(get_session)):
    return session.exec(select(Alumni)).all()


@router.patch("/{alumni_id}/verify", response_model=AlumniRead)
def verify_alumni(
    alumni_id: int,
    payload: VerifyRequest,
    session: Session = Depends(get_session),
):
    alumni = session.get(Alumni, alumni_id)
    if not alumni:
        raise HTTPException(status_code=404, detail="Alumni not found")
    alumni.status = (
        AlumniStatus.verified if payload.action == "approve" else AlumniStatus.rejected
    )
    session.add(alumni)
    session.commit()
    session.refresh(alumni)
    return alumni


@router.post("/{alumni_id}/check", response_model=CheckResult)
def check_alumni_in_external_db(
    alumni_id: int,
    session: Session = Depends(get_session),
):
    alumni = session.get(Alumni, alumni_id)
    if not alumni:
        raise HTTPException(status_code=404, detail="Alumni not found")
    external_result: ExternalCheckResponse = check_alumni(
        ime=alumni.ime,
        prezime=alumni.prezime,
        broj_indeksa=alumni.broj_indeksa,
        broj_diplome=alumni.broj_diplome,
    )
    return CheckResult(
        submitted=AlumniRead.model_validate(alumni),
        external=external_result,
    )
