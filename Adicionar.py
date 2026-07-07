from streamlit import st
from EstoqueTwo import conectar

# =====================================
# ADICIONAR
# =====================================
st.markdown("# Adicionar Produto")
st.sidebar.markdown("# Adicionar Produto")

# =====================================
# ADICIONAR PRODUTO
# =====================================

def adicionar_produto(produto, quantidade):

    conn = conectar()
    cur = conn.cursor()

    cur.execute(
        "SELECT quantidade FROM produtos WHERE nome = %s",
        (produto,)
    )

    resultado = cur.fetchone()

    if resultado:

        nova_qtd = resultado[0] + quantidade

        cur.execute(
            """
            UPDATE produtos
            SET quantidade = %s
            WHERE nome = %s
            """,
            (nova_qtd, produto)
        )

    else:

        cur.execute(
            """
            INSERT INTO produtos (
                nome,
                quantidade
            )
            VALUES (%s, %s)
            """,
            (produto, quantidade)
        )

    cur.execute(
        """
        INSERT INTO movimentacoes
        (
            produto,
            tipo,
            quantidade
        )
        VALUES
        (%s, %s, %s)
        """,
        (produto, "ENTRADA", quantidade)
    )

    conn.commit()
    cur.close()
    conn.close()


produto = st.text_input("Nome do Produto")

quantidade = st.number_input(
 "Quantidade",
        min_value=1,
        step=1
    )

if st.button("Adicionar"):

    adicionar_produto(
        produto,
        quantidade
        )

    st.success(f"{produto} salvo no banco")
    