from datetime import datetime, timedelta, time

import streamlit as st
import pandas as pd

def update_params_select_box():

  print("MUDOU SELECT BOX: {}".format(selected_day_select_box))

def update_params_date_input():

  print("MUDOU DATE_INPUT: {}".format(selected_day_date_input))

days_list = [value.strftime("%d/%m/%Y") for value in pd.date_range(datetime.today().date() - timedelta(days=100),
                                                       periods=100,
                                                       freq="D").to_pydatetime()]

selected_day_select_box = st.selectbox('Selecione a data desejada com Select Box 👇',
                                       days_list,
                                       key="value_select_box",
                                       on_change=update_params_select_box)

st.write('Data definida como:', selected_day_select_box)

selected_day_date_input = st.date_input('Selecione a data desejada com Date Input 👇',
                                        min_value=datetime.strptime((datetime.today().date() - timedelta(days=100)).strftime("%d/%m/%Y"), "%d/%m/%Y"),
key="value_date_input",
on_change=update_params_date_input)
st.write('Data definida como:', selected_day_date_input)

value_time = st.time_input('Definindo uma hora', value=time(8, 45))
st.write('Hora definida como:', value_time)

st.markdown('# Testando o Streamlit e seus widgets')

with st.expander("Sobre Widget: Expander"):
    st.markdown('''
    1. Insira um contêiner de vários elementos que pode ser expandido/recolhido.

    2. Insere um contêiner em seu aplicativo que pode ser usado para conter vários elementos e pode ser expandido ou recolhido pelo usuário. Quando recolhido, tudo o que fica visível é o rótulo fornecido.

    3. Para adicionar elementos ao contêiner retornado, você pode usar a notação "com" (preferencial) ou apenas chamar métodos diretamente no objeto retornado. Veja exemplos abaixo.

    É possível ler mais no [link](https://docs.streamlit.io/library/api-reference/layout/st.expander)

    ''')

# Sidebar
st.sidebar.header('Sobre')
st.sidebar.markdown('[Streamlit](https://streamlit.io) é uma biblioteca Python para desenvolvimento de Web Apps.')

st.sidebar.header('Para mais leituras')
st.sidebar.markdown('''
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Cheat sheet](https://docs.streamlit.io/library/cheatsheet)
- [Book](https://www.amazon.com/dp/180056550X) (Getting Started with Streamlit for Data Science)
- [Blog](https://blog.streamlit.io/how-to-master-streamlit-for-data-science/) (How to master Streamlit for data science)
''')

st.sidebar.header('Deploy')
st.sidebar.markdown('Podemos fazer deploy de Apps usando: [Streamlit Community Cloud](https://streamlit.io/cloud) in just a few clicks.')
