import streamlit as st

# Define the pages
Dashboard = st.Page("Dashboard.py", title="Dashboard", icon="📊")
Visualizar = st.Page("Visualizacao.py", title="Visualizar", icon="👀")
Adicionar = st.Page("Adicionar.py", title="Adicionar", icon="➕")
Retirar = st.Page("Retirada.py", title="Retirar", icon="🗑️")
Historico = st.Page("Historico.py", title="Histórico", icon="📜")

# Set up navigation
pg = st.navigation([Dashboard, Visualizar, Adicionar, Retirar, Historico])
