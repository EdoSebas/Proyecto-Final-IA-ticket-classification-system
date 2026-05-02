import pandas as pd, numpy as np, joblib, os, json
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE_DIR, "dataset_tickets.csv"))

# Aumenta el dataset con variaciones simples para mejorar la generalizacion.
rows = []
for _, r in df.iterrows():
    rows.append({"text": r["text"], "category": r["category"], "priority": r["priority"]})
    rows.append({"text": r["text"].upper(), "category": r["category"], "priority": r["priority"]})
    rows.append({"text": r["text"] + " necesito ayuda", "category": r["category"], "priority": r["priority"]})

df = pd.DataFrame(rows).reset_index(drop=True)
print(f"Dataset aumentado: {len(df)} registros")

X = df["text"].values
le_cat = LabelEncoder()
le_pri = LabelEncoder()
y_cat = le_cat.fit_transform(df["category"].values)
y_pri = le_pri.fit_transform(df["priority"].values)

X_train, X_test, yc_train, yc_test, yp_train, yp_test = train_test_split(
    X, y_cat, y_pri, test_size=0.2, random_state=42)

print("Entrenando red neuronal para CATEGORIA...")
# Pipeline DL: TF-IDF vectoriza el texto y MLPClassifier actua como red neuronal.
pipe_cat = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1,2), max_features=5000, sublinear_tf=True)),
    ("mlp", MLPClassifier(hidden_layer_sizes=(256,128,64), activation="relu",
        max_iter=500, random_state=42, early_stopping=True, verbose=False))
])
pipe_cat.fit(X_train, yc_train)
print(f"Accuracy categoria: {accuracy_score(yc_test, pipe_cat.predict(X_test)):.4f}")
print(classification_report(yc_test, pipe_cat.predict(X_test), target_names=le_cat.classes_))

print("Entrenando red neuronal para PRIORIDAD...")
# Se entrena un segundo modelo para predecir la prioridad del ticket.
pipe_pri = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1,2), max_features=5000, sublinear_tf=True)),
    ("mlp", MLPClassifier(hidden_layer_sizes=(256,128,64), activation="relu",
        max_iter=500, random_state=42, early_stopping=True, verbose=False))
])
pipe_pri.fit(X_train, yp_train)
print(f"Accuracy prioridad: {accuracy_score(yp_test, pipe_pri.predict(X_test)):.4f}")
print(classification_report(yp_test, pipe_pri.predict(X_test), target_names=le_pri.classes_))

models_dir = os.path.join(BASE_DIR, "models")
os.makedirs(models_dir, exist_ok=True)
# Guarda el modelo principal y los LabelEncoder para convertir IDs a etiquetas.
joblib.dump(pipe_cat, os.path.join(models_dir, "model_dl_category.pkl"))
joblib.dump(pipe_pri, os.path.join(models_dir, "model_dl_priority.pkl"))
joblib.dump(le_cat,   os.path.join(models_dir, "dl_label_encoder_category.pkl"))
joblib.dump(le_pri,   os.path.join(models_dir, "dl_label_encoder_priority.pkl"))
with open(os.path.join(models_dir, "dl_config.json"), "w") as f:
    json.dump({"categories": le_cat.classes_.tolist(), "priorities": le_pri.classes_.tolist()}, f, indent=2)
print("Modelo Deep Learning (MLP) guardado en models/")
