from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel


class Spol(str, Enum):
    M = "M"
    F = "F"
    Ostalo = "Ostalo"


class AlumniStatus(str, Enum):
    pending = "pending"
    verified = "verified"
    rejected = "rejected"


class AlumniBase(SQLModel):
    ime: str
    prezime: str
    spol: Spol
    broj_indeksa: str
    fakultet: str
    odsjek: str
    studijski_program: Optional[str] = None
    usmjerenje: Optional[str] = None
    godina_pocetka: str
    godina_zavrsetka: str
    broj_diplome: str


class Alumni(AlumniBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: AlumniStatus = AlumniStatus.pending
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AlumniCreate(AlumniBase):
    pass


class AlumniRead(AlumniBase):
    id: int
    status: AlumniStatus
    created_at: datetime


class VerifyAction(str, Enum):
    approve = "approve"
    reject = "reject"


class VerifyRequest(SQLModel):
    action: VerifyAction


class ExternalCheckData(SQLModel):
    ime: str
    prezime: str
    broj_indeksa: str
    broj_diplome: str
    fakultet: str
    odsjek: str
    godina_zavrsetka: str


class ExternalCheckResponse(SQLModel):
    found: bool
    data: Optional[ExternalCheckData] = None


class CheckResult(SQLModel):
    submitted: AlumniRead
    external: ExternalCheckResponse
