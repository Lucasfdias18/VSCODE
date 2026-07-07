import streamlit as st
from Database import carregar_estoque, conectar

# =====================================
# RETIRAR
# =====================================
st.markdown("# retirar Produto")
st.sidebar.markdown("# retirar Produto")

# =====================================
# RETIRAR PRODUTO
# =====================================

def retirar_produto(
        produto,
        quantidade,
        solicitante,
        local_retirada
):

    conn = conectar()
    cur = conn.cursor()

    cur.execute(
        "SELECT quantidade FROM produtos WHERE nome = %s",
        (produto,)
    )

    resultado = cur.fetchone()

    if not resultado:
        conn.close()
        return False, "Produto não encontrado"

    estoque = resultado[0]

    if quantidade > estoque:
        conn.close()
        return False, "Estoque insuficiente"

    novo_estoque = estoque - quantidade

    cur.execute(
        """
        UPDATE produtos
        SET quantidade = %s
        WHERE nome = %s
        """,
        (novo_estoque, produto)
    )

    cur.execute(
        """
        INSERT INTO movimentacoes
        (
            produto,
            tipo,
            quantidade,
            solicitante,
            local_retirada
        )
        VALUES
        (%s,%s,%s,%s,%s)
        """,
        (
            produto,
            "SAIDA",
            quantidade,
            solicitante,
            local_retirada
        )
    )

    conn.commit()
    cur.close()
    conn.close()

    return True, "Retirada realizada"

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