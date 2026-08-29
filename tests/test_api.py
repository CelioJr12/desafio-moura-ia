from fastapi.testclient import TestClient
from app.main import app

client_teste = TestClient(app)


def test_health():
    response = client_teste.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_pergunta_vazia():
    response = client_teste.post("/perguntar", json={"pergunta": ""})
    assert response.status_code == 400


def test_pergunta_valida_retorna_fontes():
    response = client_teste.post("/perguntar", json={"pergunta": "Quantos dias de ferias eu acumulo por mes?"})
    assert response.status_code == 200
    corpo = response.json()
    assert "resposta" in corpo
    assert "fontes" in corpo
    assert len(corpo["fontes"]) > 0