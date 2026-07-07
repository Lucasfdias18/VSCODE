from turtle import st
from EstoqueTwo import carregar_estoque, retirar_produto

# =====================================
# RETIRAR
# =====================================
st.markdown("# retirar Produto")
st.sidebar.markdown("# retirar Produto")

estoque = carregar_estoque()

st.write(estoque)

if len(estoque) == 0:

        st.warning("Nenhum produto cadastrado.")

else:

        produtos = estoque["nome"].tolist()

        produto = st.selectbox(
            "Produto",
            produtos
        )

        solicitante = st.text_input("Solicitante")

        local_retirada = st.text_input(
            "Local de retirada"
        )

        quantidade = st.number_input(
            "Quantidade",
            min_value=1
        )

        if st.button("Retirar"):

            sucesso, mensagem = retirar_produto(
                produto,
                quantidade,
                solicitante,
                local_retirada
            )

            if sucesso:
                st.success(mensagem)
            else:
                st.error(mensagem)