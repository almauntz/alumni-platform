import pytest
from unittest.mock import patch
from models import ExternalCheckData, ExternalCheckResponse

def test_register_alumni(client, alumni_data):
    response = client.post(
        "/api/alumni",
            json=alumni_data)
    assert response.status_code == 201
    assert response.json()["status"] == "pending"
    
def test_list_alumni(client, alumni_data):
    response = client.post(
        "/api/alumni",
            json=alumni_data)
    assert response.status_code == 201
    assert response.json()["status"] == "pending"
    response = client.get("/api/alumni")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["ime"] == "Ana"
    assert response.json()[0]["prezime"] == "Kovač"
    
def test_verify_approve_alumni(client, alumni_data):
        response = client.post(
            "/api/alumni",
            json=alumni_data)
        assert response.status_code == 201
        assert response.json()["status"] == "pending"
        alumni_id = response.json()["id"]
        response = client.patch(f"/api/alumni/{alumni_id}/verify",
                                json={"action": "approve"})
        assert response.status_code == 200
        assert response.json()["status"] == "verified"
    
    
def test_verify_reject_alumni(client, alumni_data):
    response = client.post(
        "/api/alumni",
        json=alumni_data)
    assert response.status_code == 201
    assert response.json()["status"] == "pending"
    alumni_id = response.json()["id"]
    response = client.patch(f"/api/alumni/{alumni_id}/verify",
                            json={"action": "reject"})
    assert response.status_code == 200
    assert response.json()["status"] == "rejected"

def test_verify_nonexistent_alumni(client):
    response = client.patch("/api/alumni/999/verify",
                            json={"action": "approve"})
    assert response.status_code == 404


def test_check_alumni_found(client, alumni_data):
    # 1. kreiraj alumni
    response = client.post("/api/alumni", json=alumni_data)
    alumni_id = response.json()["id"]
    
    # 2. mock external → found: True
    with patch("routers.alumni.check_alumni") as mock:
        mock.return_value = ExternalCheckResponse(
        found=True,
        data=ExternalCheckData(
            ime="Ana",
            prezime="Kovač",
            broj_indeksa="0123456",
            broj_diplome="D-2020-001",
            fakultet="Pravni fakultet",
            odsjek="Pravo",
            godina_zavrsetka="2020/2021"
        )
    )
        response = client.post(f"/api/alumni/{alumni_id}/check")
    
    assert response.json()["external"]["found"] == False


def test_check_alumni_not_found(client, alumni_data):
    # 1. kreiraj alumni
    response = client.post("/api/alumni", json=alumni_data)
    alumni_id = response.json()["id"]
    
    # 2. mock external → found: True
    with patch("routers.alumni.check_alumni") as mock:
        mock.return_value = ExternalCheckResponse(
        found=False,
        data=None
        )
        response = client.post(f"/api/alumni/{alumni_id}/check")
    
    assert response.json()["external"]["found"] == False