import os, json, joblib, numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")

_dl_cat = _dl_pri = _dl_le_cat = _dl_le_pri = None
_ml_cat = _ml_pri = _ml_le_cat = _ml_le_pri = None
MODEL_TYPE = None

def _load_models():
    global _dl_cat,_dl_pri,_dl_le_cat,_dl_le_pri,MODEL_TYPE
    global _ml_cat,_ml_pri,_ml_le_cat,_ml_le_pri
    try:
        _dl_cat    = joblib.load(os.path.join(MODELS_DIR,"model_dl_category.pkl"))
        _dl_pri    = joblib.load(os.path.join(MODELS_DIR,"model_dl_priority.pkl"))
        _dl_le_cat = joblib.load(os.path.join(MODELS_DIR,"dl_label_encoder_category.pkl"))
        _dl_le_pri = joblib.load(os.path.join(MODELS_DIR,"dl_label_encoder_priority.pkl"))
        MODEL_TYPE = "dl"
        print("Modelo Deep Learning (MLP) cargado.")
    except Exception as e:
        print(f"DL no disponible: {e}. Cargando RandomForest...")
        try:
            _ml_cat    = joblib.load(os.path.join(MODELS_DIR,"model_category.pkl"))
            _ml_pri    = joblib.load(os.path.join(MODELS_DIR,"model_priority.pkl"))
            _ml_le_cat = joblib.load(os.path.join(MODELS_DIR,"label_encoder_category.pkl"))
            _ml_le_pri = joblib.load(os.path.join(MODELS_DIR,"label_encoder_priority.pkl"))
            MODEL_TYPE = "ml"
            print("Modelo RandomForest cargado.")
        except Exception as e2:
            print(f"Sin modelos: {e2}")
            MODEL_TYPE = None

def predict_ticket(text: str) -> dict:
    global MODEL_TYPE
    if MODEL_TYPE is None:
        _load_models()
    if not text or not text.strip():
        return {"ai_category":"General","ai_priority":"LOW","ai_confidence":0.0,"model_used":"none"}
    try:
        if MODEL_TYPE == "dl":
            cat = _dl_le_cat.inverse_transform(_dl_cat.predict([text]))[0]
            pri = _dl_le_pri.inverse_transform(_dl_pri.predict([text]))[0]
            conf = round(float(np.max(_dl_cat.predict_proba([text])[0])), 4)
            return {"ai_category":cat,"ai_priority":pri,"ai_confidence":conf,"model_used":"deep_learning_mlp"}
        elif MODEL_TYPE == "ml":
            cat = _ml_le_cat.inverse_transform(_ml_cat.predict([text]))[0]
            pri = _ml_le_pri.inverse_transform(_ml_pri.predict([text]))[0]
            conf = round(float(np.max(_ml_cat.predict_proba([text])[0])), 4)
            return {"ai_category":cat,"ai_priority":pri,"ai_confidence":conf,"model_used":"random_forest"}
    except Exception as e:
        print(f"Error prediccion: {e}")
    t = text.lower()
    if any(w in t for w in ["error","falla","no funciona","caido"]):
        return {"ai_category":"Technical Support","ai_priority":"HIGH","ai_confidence":0.5,"model_used":"fallback"}
    elif any(w in t for w in ["factura","cobro","pago"]):
        return {"ai_category":"Billing","ai_priority":"MEDIUM","ai_confidence":0.5,"model_used":"fallback"}
    elif any(w in t for w in ["cancelar","cancelacion","baja"]):
        return {"ai_category":"Cancellations","ai_priority":"HIGH","ai_confidence":0.5,"model_used":"fallback"}
    elif any(w in t for w in ["comprar","precio","plan"]):
        return {"ai_category":"Sales","ai_priority":"LOW","ai_confidence":0.5,"model_used":"fallback"}
    return {"ai_category":"General","ai_priority":"LOW","ai_confidence":0.3,"model_used":"fallback"}
