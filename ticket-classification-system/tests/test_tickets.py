import sys, os
TICKET_PATH = os.path.join(os.path.dirname(__file__), "..", "ticket-service")
if TICKET_PATH not in sys.path:
    sys.path.insert(0, TICKET_PATH)

# Limpiar modulo src previo si existe
for key in list(sys.modules.keys()):
    if key.startswith("src"):
        del sys.modules[key]

from unittest.mock import patch, MagicMock
from datetime import datetime

with patch("src.database.create_engine") as mock_engine, \
     patch("src.models.Base.metadata.create_all"), \
     patch("src.kafka_utils.start_kafka_consumer"):
    mock_engine.return_value = MagicMock()
    from src.main import app
    from src import database
    from starlette.testclient import TestClient

def get_mock_ticket():
    t = MagicMock()
    t.id = 1
    t.title = "Problema con mi cuenta"
    t.description = "No puedo acceder"
    t.status = "OPEN"
    t.ai_category = None
    t.ai_priority = None
    t.ai_confidence = None
    t.created_at = datetime.utcnow()
    return t

def make_client(mock_session):
    app.dependency_overrides[database.get_db] = lambda: mock_session
    return TestClient(app, raise_server_exceptions=False)

def test_get_tickets_retorna_lista():
    s = MagicMock()
    s.query.return_value.offset.return_value.limit.return_value.all.return_value = []
    client = make_client(s)
    response = client.get("/tickets/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    app.dependency_overrides.clear()

def test_ticket_no_encontrado_retorna_404():
    s = MagicMock()
    s.query.return_value.filter.return_value.first.return_value = None
    client = make_client(s)
    response = client.get("/tickets/9999")
    assert response.status_code == 404
    app.dependency_overrides.clear()

def test_ticket_existente_retorna_200():
    s = MagicMock()
    s.query.return_value.filter.return_value.first.return_value = get_mock_ticket()
    client = make_client(s)
    response = client.get("/tickets/1")
    assert response.status_code == 200
    app.dependency_overrides.clear()

def test_ticket_tiene_campos_requeridos():
    s = MagicMock()
    s.query.return_value.filter.return_value.first.return_value = get_mock_ticket()
    client = make_client(s)
    response = client.get("/tickets/1")
    if response.status_code == 200:
        data = response.json()
        for campo in ["id", "title", "description", "status", "created_at"]:
            assert campo in data
    app.dependency_overrides.clear()

def test_ticket_status_inicial_es_open():
    s = MagicMock()
    s.query.return_value.filter.return_value.first.return_value = get_mock_ticket()
    client = make_client(s)
    response = client.get("/tickets/1")
    if response.status_code == 200:
        assert response.json()["status"] == "OPEN"
    app.dependency_overrides.clear()
