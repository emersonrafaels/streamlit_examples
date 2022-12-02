from os import path

import streamlit as st
from json import loads
from pandas import read_csv

# CRIANDO UM MARKDOWN
st.markdown('''
# Exibidor de arquivos

## Suba um arquivo e vejamos o que acontece :smile::heart:
''')


# CRIANDO UM WIDGET DE FILE UPLOAD
arquivo = st.file_uploader(
    'Suba seu arquivo aqui!',
    type=['jpg', 'png', 'py', 'wav', 'csv', 'json']
)

# VALIDANDO SE UM ARQUIVO FOI INSERIDO
if arquivo:

    # COM ARQUIVO INSERIDO, OBTENDO O TIPO DE ARQUIVO
    print("TIPO DO ARQUIVO: {}".format(arquivo.type))

    file, type = path.splitext(arquivo.type)
    if type in ['application', 'json']:
        st.json(loads(arquivo.read()))
    elif type in ['image', 'jpg', 'jpeg', 'png']:
        st.image(arquivo)
    elif type in ['text', 'csv']:
        df = read_csv(arquivo).transpose()
        st.dataframe(df)
        st.bar_chart(df)
    elif type in ['text', 'x-python']:
        st.code(arquivo.read().decode())
    elif type in ["audio", "wav", "mp3"]:
        st.audio(arquivo)
else:
    st.error('Ainda não tenho arquivo!')