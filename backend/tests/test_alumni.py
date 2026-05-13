import pytest
from unittest.mock import patch


def test_register_alumni(client):
    response = client.post(
        "/api/alumni",
            json={
                "ime": "Ana",
                "prezime": "Kovač",
                "spol": "F",
                "broj_indeksa": "0123456",
                "fakultet": "Pravni fakultet",
                "odsjek": "Pravo",
                "godina_pocetka": "2016/2017",
                "godina_zavrsetka": "2020/2021",
                "broj_diplome": "D-2020-001"})
    assert response.status_code == 201
    assert response.json()["status"] == "pending"
    
def test_list_alumni(client):
    response = client.post(
        "/api/alumni",
            json={
                "ime": "Ana",
                "prezime": "Kovač",
                "spol": "F",
                "broj_indeksa": "0123456",
                "fakultet": "Pravni fakultet",
                "odsjek": "Pravo",
                "godina_pocetka": "2016/2017",
                "godina_zavrsetka": "2020/2021",
                "broj_diplome": "D-2020-001"})
    assert response.status_code == 201
    assert response.json()["status"] == "pending"
    response = client.get("/api/alumni")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["ime"] == "Ana"
    assert response.json()[0]["prezime"] == "Kovač"
    