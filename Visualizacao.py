import streamlit as st
from Database import carregar_estoque
# =====================================
# VISUALIZAR
# =====================================
st.markdown("# Visualizar Estoque")
st.sidebar.markdown("# Visualizar Estoque", icon="👁️")

st.subheader("Estoque Atual")

df = carregar_estoque()

st.dataframe(df, use_container_width=True)

