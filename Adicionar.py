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

def adicionar_produto(id, produto, quantidade):

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
                id,
                nome,
                quantidade
            )
            VALUES (%s, %s, %s)
            """,
            (id, produto, quantidade)
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

opcao = st.radio(
    "Tipo de entrada",
    ["Novo Produto", "Adicionar Estoque"]
)
if opcao == "Novo Produto":

    produto = st.text_input("Nome do Produto")
    
    id = st.number_input(
        "ID do Produto",
        min_value=1,
        step=1    
    )
    quantidade = st.number_input(
        "Quantidade Inicial",
        min_value=1,
        step=1
    )
    

    if st.button("Cadastrar Produto"):

        adicionar_produto(
            id,
            produto,
            quantidade
        )

        st.success(
            f"{produto} cadastrado com sucesso!"
        )
    
elif opcao == "Adicionar Estoque":

    estoque = carregar_estoque()

    if len(estoque) == 0:

        st.warning("Nenhum produto cadastrado.")

    else:

        produtos = estoque["nome"].tolist()

        produto = st.selectbox(
            "Produto",
            produtos
        )

        quantidade = st.number_input(
            "Quantidade a adicionar",
            min_value=1,
            step=1
        )

        if st.button("Adicionar ao Estoque"):

            adicionar_produto(
                produto,
                quantidade
            )

            st.success(
                f"{quantidade} unidades adicionadas em {produto}"
            )
    