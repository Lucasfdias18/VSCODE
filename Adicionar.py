from streamlit import st
from EstoqueTwo import adicionar_produto

# =====================================
# ADICIONAR
# =====================================
st.markdown("# Adicionar Produto")
st.sidebar.markdown("# Adicionar Produto")



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

    st.success(f"{produto} salvo no banco")
    