import streamlit as st
import pandas as pd

#  st.title('Meu primeiro app para web')
#  nome = st.text_input('Quem é você?')
#  st.write('Como você vai,',nome,'?')

if 'dados' not in st.session_state:
    st.session_state.dados = pd.DataFrame ({
    'Nome': ['Ana', 'João', 'Maria'],
    'Idade': [25, 38, 22]
})

nome = st.text_input('Digite seu nome')
idade = st.number_input('Digite sua idade',min_value=0, step=1)

if st.button('Adicionar'):
    if nome:
        novo = pd.DataFrame({'Nome': [nome], 'Idade': [idade]})
        st.session_state.dados = pd.concat(
            [st.session_state.dados, novo],
            ignore_index= True
        )

        st.success('Adicionado!')
        st.snow()
    else:
        st.warning('Digite um nome')

st.dataframe(st.session_state.dados)

