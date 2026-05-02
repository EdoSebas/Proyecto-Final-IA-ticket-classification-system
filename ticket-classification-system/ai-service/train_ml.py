import pandas as pd, numpy as np, joblib, os
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE_DIR, "dataset_tickets.csv"))
print(f"Dataset: {len(df)} registros")

# X contiene los textos; y_cat/y_pri contienen las etiquetas que debe aprender el modelo.
X = df["text"].values
le_cat = LabelEncoder()
le_pri = LabelEncoder()
y_cat = le_cat.fit_transform(df["category"].values)
y_pri = le_pri.fit_transform(df["priority"].values)

X_train, X_test, yc_train, yc_test, yp_train, yp_test = train_test_split(
    X, y_cat, y_pri, test_size=0.2, random_state=42)

# Pipeline ML: TF-IDF convierte texto en numeros y RandomForest clasifica.
pipe_cat = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1,2), max_features=5000, sublinear_tf=True)),
    ("clf", RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1))
])
pipe_pri = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1,2), max_features=5000, sublinear_tf=True)),
    ("clf", RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1))
])

pipe_cat.fit(X_train, yc_train)
pipe_pri.fit(X_train, yp_train)

# Se evalua con datos de prueba que el modelo no vio durante el entrenamiento.
print(f"Accuracy categoria: {accuracy_score(yc_test, pipe_cat.predict(X_test)):.4f}")
print(f"Accuracy prioridad: {accuracy_score(yp_test, pipe_pri.predict(X_test)):.4f}")

models_dir = os.path.join(BASE_DIR, "models")
os.makedirs(models_dir, exist_ok=True)
# Guarda modelos y codificadores para usarlos luego desde ai-service/src/model.py.
joblib.dump(pipe_cat, os.path.join(models_dir, "model_category.pkl"))
joblib.dump(pipe_pri, os.path.join(models_dir, "model_priority.pkl"))
joblib.dump(le_cat,   os.path.join(models_dir, "label_encoder_category.pkl"))
joblib.dump(le_pri,   os.path.join(models_dir, "label_encoder_priority.pkl"))
print("Modelos ML guardados en models/")
