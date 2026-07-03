import streamlit as st
import pandas as pd
import os

ARQUIVO = "estoque.csv"

# Cria arquivo se não existir
if not os.path.exists(ARQUIVO):
    df = pd.DataFrame(columns=["Produto", "Quantidade"])
    df.to_csv(ARQUIVO, index=False)

# Ler estoque
df = pd.read_csv(ARQUIVO)

st.title("📦 Controle de Estoque")

menu = st.sidebar.selectbox(
    "Menu",
    ["Visualizar", "Adicionar Produto", "Retirar Produto"]
)

# Visualizar
if menu == "Visualizar":
    st.subheader("Estoque Atual")
    st.dataframe(df)

# Adicionar Produto
elif menu == "Adicionar Produto":
    produto = st.text_input("Nome do Produto")
    quantidade = st.number_input("Quantidade", min_value=1)

    if st.button("Adicionar"):

        if produto in df["Produto"].values:
            df.loc[df["Produto"] == produto, "Quantidade"] += quantidade
        else:
            novo = pd.DataFrame({
                "Produto": [produto],
                "Quantidade": [quantidade]
            })
            df = pd.concat([df, novo], ignore_index=True)

        df.to_csv(ARQUIVO, index=False)
        st.success("Produto adicionado com sucesso!")

# Retirada
elif menu == "Retirar Produto":

    produtos = df["Produto"].tolist()

    if produtos:

        produto = st.selectbox("Produto", produtos)

        solicitante = st.text_input("Solicitante")

        quantidade = st.number_input(
            "Quantidade para retirada",
            min_value=1
        )

        if st.button("Retirar"):

            estoque_atual = df.loc[
                df["Produto"] == produto,
                "Quantidade"
            ].values[0]

            if quantidade > estoque_atual:
                st.error("Estoque insuficiente.")
            else:
                df.loc[
                    df["Produto"] == produto,
                    "Quantidade"
                ] -= quantidade

                df.to_csv(ARQUIVO, index=False)

                st.success(
                    f"Retirada realizada por {solicitante}"
                )