import random

CATEGORIES = ["Billing", "Technical Support", "Sales", "Cancellations"]
PRIORITIES = ["HIGH", "MEDIUM", "LOW"]

def predict_ticket(text: str):
    """
    Mock classification model.
    In a real scenario, this would load a DistilBERT or TF-IDF model.
    """
    text_lower = text.lower()
    
    # Heurística simple para simular predicciones de un modelo real
    if "error" in text_lower or "no puedo" in text_lower or "falla" in text_lower:
        category = "Technical Support"
        priority = "HIGH"
    elif "pago" in text_lower or "factura" in text_lower or "cobro" in text_lower:
        category = "Billing"
        priority = "MEDIUM"
    elif "comprar" in text_lower or "precio" in text_lower or "info" in text_lower:
        category = "Sales"
        priority = "LOW"
    else:
        category = random.choice(CATEGORIES)
        priority = random.choice(PRIORITIES)
        
    confidence = round(random.uniform(0.70, 0.99), 2)
    
    return {
        "ai_category": category,
        "ai_priority": priority,
        "ai_confidence": confidence
    }
