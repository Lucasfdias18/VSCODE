
# =====================================
# DASHBOARD
# =====================================
import streamlit as st
import plotly.express as px
import pandas as pd
from Database import conectar

st.markdown("# Dashboard")
st.sidebar.markdown("# Dashboard")

st.subheader("📊 Dashboard de Consumo")

conn = conectar()

movimentacoes = pd.read_sql("""
        SELECT
            data,
            produto,
            tipo,
            quantidade
        FROM movimentacoes
        WHERE tipo = 'SAIDA'
        ORDER BY data
    """, conn)

conn.close()

if movimentacoes.empty:

        st.warning("Nenhuma retirada registrada.")

else:

        # ----------------------
        # Total por produto
        # ----------------------
        total_produto = (
            movimentacoes
            .groupby("produto")["quantidade"]
            .sum()
            .reset_index()
        )

        fig_produto = px.bar(
            total_produto,
            x="produto",
            y="quantidade",
            title="Quantidade Retirada por Produto",
            color="quantidade"
        )

        st.plotly_chart(
            fig_produto,
            use_container_width=True
        )

        # ----------------------
        # Consumo no tempo
        # ----------------------
        movimentacoes["data"] = pd.to_datetime(
            movimentacoes["data"]
        )

        consumo_dia = (
            movimentacoes
            .groupby(
                movimentacoes["data"].dt.date
            )["quantidade"]
            .sum()
            .reset_index()
        )

        fig_tempo = px.line(
            consumo_dia,
            x="data",
            y="quantidade",
            markers=True,
            title="Evolução do Consumo"
        )

        st.plotly_chart(
            fig_tempo,
            use_container_width=True
        )

        # ----------------------
        # Top produtos
        # ----------------------
        st.subheader("🏆 Produtos Mais Retirados")

        st.dataframe(
            total_produto
            .sort_values(
                by="quantidade",
                ascending=False
            ),
            use_container_width=True
        )

        # ----------------------
        # Pico de Retirada
        # ----------------------
        pico = consumo_dia.loc[
            consumo_dia["quantidade"].idxmax()
        ]

        st.metric(
            "🔥 Maior Pico Diário",
            f"{int(pico['quantidade'])} unidades",
            str(pico["data"])
        )