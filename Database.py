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
            CREATE TABLE produtos (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(200) UNIQUE NOT NULL,
        quantidade INTEGER NOT NULL
        );
        """)

    cur.execute("""
            CREATE TABLE movimentacoes (
        id SERIAL PRIMARY KEY,
        produto VARCHAR(200),
        tipo VARCHAR(20),
        quantidade INTEGER,
        solicitante VARCHAR(200),
        local_retirada VARCHAR(200),
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
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
        "SELECT * FROM produtos",
        conn
    )
    
    conn.close()

    return df









