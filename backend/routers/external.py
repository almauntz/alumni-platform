from fastapi import APIRouter
from models import ExternalCheckData, ExternalCheckResponse

router = APIRouter()

# Simulated university database records — replace with real HTTP call later
_MOCK_DB: list[dict] = [
    {
        "ime": "Ana",
        "prezime": "Kovač",
        "broj_indeksa": "0123456",
        "broj_diplome": "D-2020-001",
        "fakultet": "Pravni fakultet",
        "odsjek": "Pravo",
        "godina_zavrsetka": "2020/2021",
    },
    {
        "ime": "Emir",
        "prezime": "Husić",
        "broj_indeksa": "0654321",
        "broj_diplome": "D-2015-042",
        "fakultet": "Ekonomski fakultet",
        "odsjek": "Menadžment",
        "godina_zavrsetka": "2015/2016",
    },
]


@router.get("/check", response_model=ExternalCheckResponse)
def check_alumni(
    ime: str,
    prezime: str,
    broj_indeksa: str,
    broj_diplome: str,
):
    for record in _MOCK_DB:
        if (
            record["broj_indeksa"] == broj_indeksa
            and record["broj_diplome"] == broj_diplome
        ):
            return ExternalCheckResponse(
                found=True,
                data=ExternalCheckData(**record),
            )
    return ExternalCheckResponse(found=False, data=None)
