from turtle import st
from EstoqueTwo import carregar_historico


# =====================================
# HISTÓRICO
# =====================================
st.markdown("# Histórico")
st.sidebar.markdown("# Histórico")

st.subheader("Histórico de Movimentações")

historico = carregar_historico()

st.dataframe(
        historico,
        use_container_width=True
    )