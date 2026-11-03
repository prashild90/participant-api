from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all():
    r = client.get("/participants")
    assert r.status_code == 200

def test_create():
    r = client.post("/participants", json={"name":"Test","age":25,"site":"KTM"})
    assert r.status_code == 200   
