import streamlit as st

st.set_page_config(
    page_title="Storytelling - Passos Mágicos",
    page_icon="📘",
    layout="centered"
)

st.title("📘 Storytelling — Projeto Passos Mágicos")
st.caption("Tech Challenge 5 • Datathon • Modelo preditivo de risco de defasagem")

st.divider()

# =========================================================
# 1) PROBLEMA
# =========================================================
st.header("1) O problema")
st.markdown(
    """
    A **defasagem escolar** não surge de forma abrupta.  
    Ela é precedida por sinais comportamentais, emocionais e acadêmicos.

    A análise exploratória mostrou que:

    - O desempenho acadêmico mantém estabilidade ao longo dos anos
    - O engajamento está diretamente associado ao desempenho
    - O ponto de virada (IPV) apresenta forte relação com evolução acadêmica

    A ONG **Passos Mágicos** precisa identificar alunos mais vulneráveis
    para agir de forma preventiva.
    """
)

st.divider()

# =========================================================
# 2) OBJETIVO
# =========================================================
st.header("2) Objetivo da solução")
st.markdown(
    """
    Desenvolver um modelo capaz de estimar a **probabilidade de um aluno
    apresentar baixo desempenho acadêmico**, apoiando decisões pedagógicas.

    O foco é oferecer:

    - Probabilidade de risco
    - Classificação em baixo / moderado / alto risco
    - Ferramenta interpretável e aplicável em produção
    """
)

st.divider()

# =========================================================
# 3) DADOS
# =========================================================
st.header("3) Dados utilizados")
st.markdown(
    """
    A base contém informações educacionais de **2022 a 2024**, incluindo:

    - IAN (adequação)
    - IDA (desempenho acadêmico)
    - IEG (engajamento)
    - IAA (autoavaliação)
    - IPS (psicossocial)
    - IPV (ponto de virada)
    - Idade

    Esses indicadores capturam dimensões cognitivas e comportamentais
    do desenvolvimento do aluno.
    """
)

st.divider()

# =========================================================
# 4) DEFINIÇÃO DO RISCO
# =========================================================
st.header("4) Definição de risco (target)")
st.markdown(
    """
    O risco foi definido como:

    **Alunos com IDA abaixo do percentil 25 da base histórica.**

    Essa abordagem permite identificar os casos mais vulneráveis
    dentro do contexto analisado.

    Importante:
    - O IDA foi usado apenas para definir o risco.
    - Ele não é utilizado como variável explicativa no modelo.
    """
)

st.divider()

# =========================================================
# 5) MODELO UTILIZADO
# =========================================================
st.header("5) Modelo utilizado")
st.markdown(
    """
    Foi utilizada **Regressão Logística com Elastic Net**, por ser:

    - Interpretável
    - Estável
    - Robusta para dados tabulares
    - Adequada para aplicação em produção (Streamlit)

    As variáveis utilizadas no modelo foram:

    - Idade
    - IAN
    - IEG
    - IAA
    - IPS
    - IPV
    """
)

st.divider()

# =========================================================
# 6) RESULTADOS
# =========================================================
st.header("6) Resultados")

st.markdown(
    """
    O modelo apresentou capacidade moderada de discriminação entre alunos
    em risco e não risco.
    """
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**ROC AUC**")
    st.caption("≈ 0.79")

with col2:
    st.markdown("**Principal variável**")
    st.caption("IPV")

with col3:
    st.markdown("**Aplicação**")
    st.caption("Triagem preventiva")

st.markdown(
    """
    📌 **Insight principal:**
    O indicador de ponto de virada (IPV) apresentou o maior peso no modelo,
    seguido por engajamento (IEG) e autoavaliação (IAA).

    Isso indica que fatores comportamentais possuem forte associação
    com risco de baixo desempenho.
    """
)

st.subheader("📊 Curva ROC")
st.image("assets/roc_curve.png",
    caption="Curva ROC do modelo de regressão logística",
    use_container_width=True
)
st.markdown(
"""
A curva ROC demonstra a capacidade do modelo em distinguir alunos
em risco e não risco. 

Com AUC ≈ 0.79, o modelo apresenta boa separação estatística,
sendo adequado para triagem preventiva.
"""
)

st.subheader("📊 Importância das variáveis")
st.image(
    "../assets/roc_curve.png",
    caption="Curva ROC do modelo de regressão logística",
    width="stretch"
)

st.divider()

# =========================================================
# 7) PRODUTO ENTREGUE
# =========================================================
st.header("7) Produto entregue")
st.markdown(
    """
    Foi desenvolvido um aplicativo em Streamlit que permite:

    - Inserir dados atuais do aluno
    - Estimar probabilidade de risco
    - Classificar em baixo / moderado / alto risco
    - Apoiar decisões pedagógicas preventivas

    A solução é leve, interpretável e pronta para uso.
    """
)

st.divider()

# =========================================================
# 8) IMPACTO ESPERADO
# =========================================================
st.header("8) Impacto esperado para a ONG")
st.markdown(
    """
    A ferramenta permite:

    - Identificação antecipada de alunos vulneráveis
    - Priorização pedagógica
    - Melhor alocação de recursos
    - Monitoramento contínuo de risco

    O modelo não substitui avaliação pedagógica,
    mas atua como apoio à tomada de decisão.
    """
)
st.caption(
"⚠️ Este modelo identifica padrões estatísticos e não substitui avaliação pedagógica individual."
)

st.divider()

# =========================================================
# 9) PRÓXIMOS PASSOS
# =========================================================
st.header("9) Próximos passos")
st.markdown(
    """
    Evoluções recomendadas:

    - Ajustar limiares de risco conforme estratégia pedagógica
    - Monitorar drift anual dos indicadores
    - Expandir modelo com dados longitudinais
    - Criar dashboards agregados por turma e instituição
    """
)
