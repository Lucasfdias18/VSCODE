from streamlit import st
from EstoqueTwo import carregar_estoque
# =====================================
# VISUALIZAR
# =====================================
st.markdown("# Visualizar Estoque")
st.sidebar.markdown("# Visualizar Estoque")

st.subheader("Estoque Atual")

df = carregar_estoque()

st.dataframe(df, use_container_width=True)

