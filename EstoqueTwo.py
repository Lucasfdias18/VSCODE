import streamlit as st
import pandas as pd
import psycopg2


# =====================================
# CONFIGURAÇÃO DO POSTGRESQL
# =====================================

DATABASE_URL = "postgresql://postgres.mgickjwfczdfxbnyflbr:EstoquePLUS@aws-1-sa-east-1.pooler.supabase.com:5432/postgres"
#EstoquePLUS@2026
def conectar():
    return psycopg2.connect(DATABASE_URL)

# =====================================
# CRIAR TABELAS
# =====================================

def criar_tabelas():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(200) UNIQUE NOT NULL,
            quantidade INTEGER NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id SERIAL PRIMARY KEY,
            produto VARCHAR(200),
            tipo VARCHAR(20),
            quantidade INTEGER,
            solicitante VARCHAR(200),
            local_retirada VARCHAR(200),
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

criar_tabelas()

# =====================================
# CARREGAR ESTOQUE
# =====================================

def carregar_estoque():
    conn = conectar()

    df = pd.read_sql(
        "SELECT nome AS Produto, quantidade AS Quantidade FROM produtos",
        conn
    )

    conn.close()

    return df

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

# =====================================
# HISTÓRICO
# =====================================

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

# =====================================
# INTERFACE
# =====================================

st.title("📦 Controle de Estoque")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Visualizar Estoque",
        "Adicionar Produto",
        "Retirar Produto",
        "Histórico"
    ]
)

# =====================================
# VISUALIZAR
# =====================================

if menu == "Visualizar Estoque":

    st.subheader("Estoque Atual")

    df = carregar_estoque()

    st.dataframe(df, use_container_width=True)

# =====================================
# ADICIONAR
# =====================================

elif menu == "Adicionar Produto":

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

        st.success(
            "Produto adicionado com sucesso!"
        )

# =====================================
# RETIRAR
# =====================================

elif menu == "Retirar Produto":

    estoque = carregar_estoque()

    produtos = estoque["Produto"].tolist()

    if produtos:

        produto = st.selectbox(
            "Produto",
            produtos
        )

        solicitante = st.text_input(
            "Solicitante"
        )

        local_retirada = st.text_input(
            "Local de retirada"
        )

        quantidade = st.number_input(
            "Quantidade",
            min_value=1,
            step=1
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

# =====================================
# HISTÓRICO
# =====================================

elif menu == "Histórico":

    st.subheader("Histórico de Movimentações")

    historico = carregar_historico()

    st.dataframe(
        historico,
        use_container_width=True
    )