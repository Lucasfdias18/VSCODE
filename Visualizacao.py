# =====================================
# VISUALIZAR
# =====================================
st.markdown("# Visualizar Estoque")
st.sidebar.markdown("# Visualizar Estoque")

from streamlit import st

from EstoqueTwo import carregar_estoque


st.subheader("Estoque Atual")

df = carregar_estoque()

st.dataframe(df, use_container_width=True)

