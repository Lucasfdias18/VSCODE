import streamlit as st
import pandas as pd
from Database import conectar


# =====================================
# HISTÓRICO
# =====================================
st.markdown("# Histórico")
st.sidebar.markdown("# Histórico", icon="📜")

def carregar_historico():

    conn = conectar()

    df = pd.read_sql("""
        SELECT
            data,
            produto,
            tipo,
            quantidade,
            solicitante,
            local_retirada
        FROM movimentacoes
        ORDER BY data DESC
    """, conn)

    conn.close()

    return df
st.subheader("Histórico de Movimentações")

historico = carregar_historico()

st.dataframe(
        historico,
        use_container_width=True
    )