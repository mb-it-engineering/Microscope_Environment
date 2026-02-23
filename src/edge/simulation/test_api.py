from fastapi.testclient import TestClient
from edge.simulation.api import app

client = TestClient(app)

def test_capture():
    response = client.post("/execute/capture")
    assert response.status_code == 200
    assert "result" in response.json()

def test_set_parameter():
    response = client.post("/execute/set_parameter", json={"name": "exposure", "value": 60})
    assert response.status_code == 200
    assert response.json()["result"]["status"] == "ok"

def test_get_parameters():
    response = client.post("/execute/get_parameters")
    assert response.status_code == 200
    assert "exposure" in response.json()["result"]

def test_reset():
    response = client.post("/execute/reset")
    assert response.status_code == 200
    assert response.json()["result"]["status"] == "ok"