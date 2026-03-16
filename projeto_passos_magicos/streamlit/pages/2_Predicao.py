#%% IMPORTAÇÕES E PATH
import streamlit as st
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = BASE_DIR / "src"
sys.path.append(str(SRC_DIR))

from teste_predicao import predict_single


#%% CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Risco de Defasagem Escolar",
    page_icon="📘",
    layout="centered"
)

st.title("📘 Avaliação de Risco de Defasagem Escolar")
st.markdown(
    """
    Esta ferramenta utiliza **Machine Learning** para **identificar alunos
    com risco de defasagem**, apoiando decisões pedagógicas **preventivas**.
    """
)

st.divider()


#%%FORMULÁRIO
st.subheader("📋 Dados do aluno")

with st.form("form_aluno"):

    idade = st.number_input(
        "Idade",
        min_value=6,
        max_value=20,
        value=14,
        step=1
    )

    st.subheader("📊 Indicadores Educacionais")
    ian  = st.number_input("IAN",  0.0, 10.0, 6.0, 0.1)
    ieg  = st.number_input("IEG (Engajamento)", 0.0, 10.0, 6.0, 0.1)
    iaa  = st.number_input("IAA",  0.0, 10.0, 6.0, 0.1)
    ips  = st.number_input("IPS",  0.0, 10.0, 6.0, 0.1)
    ipv  = st.number_input("IPV",  0.0, 10.0, 6.0, 0.1)

    submitted = st.form_submit_button("🔍 Avaliar risco")


# PROCESSAMENTO E RESULTADO
if submitted:

    aluno = {
        "idade": idade,
        "ian": ian,
        "ieg": ieg,
        "iaa": iaa,
        "ips": ips,
        "ipv": ipv}

    resultado = predict_single(aluno)
    prob = resultado["prob_risco"]

    st.divider()
    st.subheader("📈 Resultado da Avaliação")

    st.metric(
        label="Probabilidade de risco",
        value=f"{prob * 100:.1f}%"
    )

    # INTERPRETAÇÃO PEDAGÓGICA
    if prob < 0.4:
        st.success("🟢 Baixo risco de defasagem")
        st.markdown(
            "O aluno apresenta **bom desempenho geral**. "
            "Recomenda-se manter o acompanhamento pedagógico regular."
        )

    elif prob < 0.7:
        st.warning("🟡 Risco moderado de defasagem")
        st.markdown(
            "O aluno merece **atenção preventiva**, especialmente em aspectos "
            "de engajamento ou socioemocionais."
        )

    else:
        st.error("🔴 Alto risco de defasagem")
        st.markdown(
            "O aluno apresenta **alto risco** e deve ser **priorizado para "
            "intervenção pedagógica estruturada**."
        )