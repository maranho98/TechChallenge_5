#%%
import pandas as pd
import numpy as np
import re
import warnings
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

warnings.filterwarnings("ignore")

#%%
def consolidar_colunas_duplicadas(df, nome_coluna):
    colunas = [c for c in df.columns if c == nome_coluna]
    if len(colunas) > 1:
        df[nome_coluna] = df[colunas].bfill(axis=1).iloc[:, 0]
        df = df.drop(columns=colunas[1:])
    return df


def converter_para_numerico(df, colunas):
    for col in colunas:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.extract(r"(\d+)", expand=False)
                .astype(float)
            )
    return df


def normaliza_fase(valor):
    if pd.isna(valor):
        return np.nan
    valor = str(valor).upper()
    if "ALFA" in valor:
        return 0
    m = re.search(r"(\d+)", valor)
    return int(m.group(1)) if m else np.nan


def normaliza_idade(valor):
    if pd.isna(valor):
        return np.nan
    valor = str(valor)
    m = re.search(r"(\d+)", valor)
    return float(m.group(1)) if m else np.nan


#%%
CAMINHO = "data/BASE_DE_DADOS_PEDE_2024_DATATHON.xlsx"

aba22 = pd.read_excel(CAMINHO, sheet_name="PEDE2022")
aba23 = pd.read_excel(CAMINHO, sheet_name="PEDE2023")
aba24 = pd.read_excel(CAMINHO, sheet_name="PEDE2024")

aba22["ano_origem"] = 2022
aba23["ano_origem"] = 2023
aba24["ano_origem"] = 2024

#%%
rename_2022 = {
    "RA": "id_aluno", "Idade 22": "idade", "Turma": "turma",
    "Gênero": "genero", "Ano ingresso": "ano_ingresso",
    "Instituição de ensino": "instituicao_ensino",
    "Fase": "fase_atual", "Fase ideal": "fase_ideal",
    "Defas": "defasagem", "INDE 22": "inde",
    "IAN": "ian", "IDA": "ida", "IEG": "ieg",
    "IAA": "iaa", "IPS": "ips", "IPV": "ipv",
    "Matem": "nota_matematica", "Portug": "nota_portugues",
    "Inglês": "nota_ingles", "Atingiu PV": "atingiu_ponto_virada",
    "Indicado": "indicado_bolsa"
}

rename_2023 = {
    "RA": "id_aluno", "Idade": "idade", "Turma": "turma",
    "Gênero": "genero", "Ano ingresso": "ano_ingresso",
    "Instituição de ensino": "instituicao_ensino",
    "Fase": "fase_atual", "Fase Ideal": "fase_ideal",
    "Defasagem": "defasagem", "INDE 2023": "inde",
    "IAN": "ian", "IDA": "ida", "IEG": "ieg",
    "IAA": "iaa", "IPS": "ips", "IPV": "ipv",
    "Mat": "nota_matematica", "Por": "nota_portugues",
    "Ing": "nota_ingles", "Atingiu PV": "atingiu_ponto_virada",
    "Indicado": "indicado_bolsa"
}

rename_2024 = {
    "RA": "id_aluno", "Idade": "idade", "Turma": "turma",
    "Gênero": "genero", "Ano ingresso": "ano_ingresso",
    "Instituição de ensino": "instituicao_ensino",
    "Fase": "fase_atual", "Fase Ideal": "fase_ideal",
    "Defasagem": "defasagem", "INDE 2024": "inde",
    "IAN": "ian", "IDA": "ida", "IEG": "ieg",
    "IAA": "iaa", "IPS": "ips", "IPV": "ipv",
    "Mat": "nota_matematica", "Por": "nota_portugues",
    "Ing": "nota_ingles", "Atingiu PV": "atingiu_ponto_virada",
    "Indicado": "indicado_bolsa"
}


#%%
aba22 = aba22.rename(columns=rename_2022)
aba23 = aba23.rename(columns=rename_2023)
aba24 = aba24.rename(columns=rename_2024)

aba23 = consolidar_colunas_duplicadas(aba23, "obs_ipv")

dados = pd.concat([aba22, aba23, aba24], ignore_index=True)
dados.columns = [c.lower() for c in dados.columns]


#%%
inds = ["ian", "ida", "ieg", "iaa", "ips", "ipv", "inde"]
notas = ["nota_matematica", "nota_portugues", "nota_ingles"]

dados = converter_para_numerico(dados, inds + notas)

dados["idade"] = dados["idade"].apply(normaliza_idade)
dados["idade"] = dados["idade"].fillna(dados["idade"].median())

dados["fase_atual"] = dados["fase_atual"].apply(normaliza_fase)
dados["fase_ideal"] = dados["fase_ideal"].apply(normaliza_fase)

dados["score_cognitivo"] = dados[["inde", "ian", "nota_matematica", "nota_portugues", "nota_ingles"]].mean(axis=1)

dados["score_engajamento"] = dados["ieg"]

dados["score_socioemocional"] = dados[["ips", "ipv", "iaa"]].mean(axis=1)


#%%
dados["risco_defasagem"] = np.where(dados["ida"] < dados["ida"].quantile(0.25),1, 0)


#%%
features_numericas = [
    "idade",
    "ian",
    "iaa",
    "ips",
    "ipv"
]

df_ml = dados.copy()

for col in features_numericas:
    df_ml[col] = df_ml[col].fillna(df_ml[col].median())

X = df_ml[features_numericas]
y = df_ml["risco_defasagem"]

#%%
X_train, _, y_train, _ = train_test_split(
    X, y, stratify=y, test_size=0.25, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

modelo = LogisticRegression(
    penalty="elasticnet",
    solver="saga",
    l1_ratio=0.3,
    C=1.0,
    max_iter=5000,
    random_state=42
)

modelo.fit(X_train_scaled, y_train)

#%%
joblib.dump(modelo, "models/lr_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")