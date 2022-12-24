from json import loads

import streamlit as st
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

    match arquivo.type.split('/'):
        case 'application', 'json':
            st.json(loads(arquivo.read()))
        case 'image', _:
            st.image(arquivo)
        case 'text', 'csv':
            df = read_csv(arquivo).transpose()
            st.dataframe(df)
            st.bar_chart(df)
        case 'text', 'x-python':
            st.code(arquivo.read().decode())
        case 'audio', _:
            st.audio(arquivo)
else:
    st.error('Ainda não tenho arquivo!')