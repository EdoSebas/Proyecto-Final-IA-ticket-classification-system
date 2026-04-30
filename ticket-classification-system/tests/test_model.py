import sys, os
AI_PATH = os.path.join(os.path.dirname(__file__), "..", "ai-service")
if AI_PATH not in sys.path:
    sys.path.insert(0, AI_PATH)

for key in list(sys.modules.keys()):
    if key.startswith("src"):
        del sys.modules[key]

from src.model import predict_ticket

def test_prediccion_soporte_tecnico():
    result = predict_ticket("No puedo acceder a mi cuenta")
    assert result["ai_category"] == "Technical Support"
    assert result["ai_priority"] in ["HIGH", "MEDIUM", "LOW"]
    assert 0.0 <= result["ai_confidence"] <= 1.0

def test_prediccion_facturacion():
    result = predict_ticket("Me cobraron dos veces el mismo mes")
    assert result["ai_category"] == "Billing"
    assert result["ai_confidence"] >= 0.0

def test_prediccion_cancelacion():
    result = predict_ticket("Quiero cancelar mi suscripcion")
    assert result["ai_category"] == "Cancellations"
    assert result["ai_priority"] in ["HIGH", "MEDIUM", "LOW"]

def test_prediccion_ventas():
    result = predict_ticket("Quiero informacion sobre los planes disponibles")
    assert result["ai_category"] == "Sales"

def test_texto_vacio():
    result = predict_ticket("")
    assert result["ai_category"] == "General"
    assert result["ai_priority"] == "LOW"
    assert result["ai_confidence"] == 0.0

def test_campos_requeridos():
    result = predict_ticket("Tengo un problema con mi cuenta")
    assert "ai_category" in result
    assert "ai_priority" in result
    assert "ai_confidence" in result
    assert "model_used" in result

def test_confidence_rango_valido():
    result = predict_ticket("El sistema no funciona")
    assert 0.0 <= result["ai_confidence"] <= 1.0
