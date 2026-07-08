import streamlit as st
from Database import carregar_estoque, conectar

# =====================================
# ADICIONAR
# =====================================
st.markdown("# Adicionar Produto")
st.sidebar.markdown("# Adicionar Produto ")

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

estoque = carregar_estoque()
produtos = estoque["nome"].tolist()
if st.button("Novo Produto"):
    produto = st.text_input(
        "Novo Produto"
    )    
    quantidade = st.number_input(
        "Quantidade",
        min_value=1,
        step=1
    )
else:
    produto = st.selectbox(
    "Produto",
     produtos
)

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
    