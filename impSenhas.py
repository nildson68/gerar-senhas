import streamlit as st

# Inicialização do estado da sessão
if 'normal' not in st.session_state:
    st.session_state.normal = 0

if 'prioritaria' not in st.session_state:
    st.session_state.prioritaria = 0

st.title("🎟️ Imprima sua Senha")

st.write("Clique em um dos botões abaixo para gerar uma nova senha:")

col1, col2 = st.columns(2)

# Botão para senha normal
with col1:
    if st.button("Gerar Senha Normal (N)"):
        st.session_state.normal += 1
        senha_gerada = f"N{st.session_state.normal:03d}"
        st.success(f"Senha Gerada: **{senha_gerada}**")

# Botão para senha prioritária
with col2:
    if st.button("Gerar Senha Prioritária (P)"):
        st.session_state.prioritaria += 1
        senha_gerada = f"P{st.session_state.prioritaria:03d}"
        st.success(f"Senha Gerada: **{senha_gerada}**")

# Simula a impressão (exibe na tela como um ticket)
if 'senha_gerada' in locals():
    st.markdown("---")
    st.markdown("### 🖨️ Ticket de Senha")
    st.code(f"""
+----------------------+
|      SUA SENHA       |
|                      |
|       {senha_gerada}          |
|                      |
+----------------------+
    """, language="text")
