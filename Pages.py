import streamlit as st

st.set_page_config(
    page_title="Estoque Two",
    page_icon="📦"
)

Dashboard = st.Page("Dashboard.py", title="Dashboard", icon="📊")
Visualizar = st.Page("Visualizacao.py", title="Visualizar", icon="👁️")
Adicionar = st.Page("Adicionar.py", title="Adicionar", icon="➕")
Retirar = st.Page("Retirada.py", title="Retirar", icon="📦")
Historico = st.Page("Historico.py", title="Histórico", icon="📜")

pg = st.navigation([
    Dashboard,
    Visualizar,
    Adicionar,
    Retirar,
    Historico
])

pg.run()