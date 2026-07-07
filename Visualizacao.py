# =====================================
# VISUALIZAR
# =====================================
st.markdown("# Visualizar Estoque")
st.sidebar.markdown("# Visualizar Estoque")

from turtle import st

from EstoqueTwo import carregar_estoque


st.subheader("Estoque Atual")

df = carregar_estoque()

st.dataframe(df, use_container_width=True)

