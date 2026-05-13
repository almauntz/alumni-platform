import httpx
from fastapi import APIRouter, HTTPException
from models import ExternalCheckData, ExternalCheckResponse

router = APIRouter()

EXTERNAL_API_URL = "https://api.alumni.untz.ba/alumni/check"


@router.get("/check", response_model=ExternalCheckResponse)
def check_alumni(
    ime: str,
    prezime: str,
    broj_indeksa: str,
    broj_diplome: str,
):
    try:
        response = httpx.get(
            EXTERNAL_API_URL,
            params={
                "ime": ime,
                "prezime": prezime,
                "broj_indeksa": broj_indeksa,
                "broj_diplome": broj_diplome,
            },
            timeout=10.0,
        )
        response.raise_for_status()
        payload = response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return ExternalCheckResponse(found=False, data=None)
        raise HTTPException(status_code=502, detail="External API error")
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="External API unreachable")

    if not payload.get("found"):
        return ExternalCheckResponse(found=False, data=None)

    return ExternalCheckResponse(
        found=True,
        data=ExternalCheckData(**payload["data"]),
    )
