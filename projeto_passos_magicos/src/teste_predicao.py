import numpy as np
import pandas as pd
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH  = BASE_DIR / "models" / "lr_model.pkl"
SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"

modelo = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

def normaliza_fase(valor):
    if pd.isna(valor):
        return np.nan
    valor = str(valor).upper()
    if "ALFA" in valor:
        return 0
    import re
    m = re.search(r"(\d+)", valor)
    return int(m.group(1)) if m else np.nan

FEATURES_NUMERICAS = [
    "idade","ian","iaa","ips","ipv"
]

def predict_single(aluno: dict):
    """
    aluno: dicionário com os dados de UM aluno
    """

    df = pd.DataFrame([aluno])

    # ---------- Numéricas ----------
    X = df[FEATURES_NUMERICAS]

    X_scaled = scaler.transform(X)

    prob_risco = modelo.predict_proba(X_scaled)[0,1]
    classe = int(prob_risco >= 0.5)

    return {
        "prob_risco": float(prob_risco),
        "classe_risco": classe
    }