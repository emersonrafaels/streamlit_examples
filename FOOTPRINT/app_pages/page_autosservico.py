import pandas as pd
import streamlit as st
from dynaconf import settings
from streamlit_folium import st_folium

from utils.pandas_functions import load_data, convert_dataframe_to_aggrid
from utils.map_functions import load_map


def load_autosservico():
    # INICIANDO A VARIÁVEL QUE CONTROLA O RAIO DE SOMBREAMENTO
    raio_sombreamento = 0

    # CARREGANDO DATAFRAME
    df_footprint = load_data(data_dir=settings.DATA_DIR_AGENCIAS)

    # INCLUINDO O DATAFRAME EM TELA
    st.markdown("### Autosserviço - Dados do footprint")
    dataframe_aggrid = convert_dataframe_to_aggrid(data=df_footprint)

    # OBTENDO O DATAFRAME DAS LINHAS SELECIONADAS
    selected_df = pd.DataFrame(dataframe_aggrid["selected_rows"])

    # INCLUINDO NO APP
    st.markdown("### Parque de agências")
    st_col1, st_col2 = st.columns(2)
    with st_col1:
        result_view_sombreamento = st.checkbox(
            "Visualizar sombreamento",
            value=False,
            key=None,
            help="Habilita o controle de sombreamento sobre o mapa",
            on_change=None,
            disabled=False,
            label_visibility="visible",
        )
    if result_view_sombreamento:
        with st_col2:
            raio_sombreamento = st.slider(
                "Raio desejado (em km):",
                min_value=0,
                max_value=1000,
                step=1,
                help="O raio é aplicado sobre o mapa",
            )

    # CRIANDO MAPA
    mapobj = load_map(
        data=selected_df, circle_radius=raio_sombreamento, validator_add_layer=True
    )

    # INCLUINDO O MAPA NO APP
    st_data = st_folium(mapobj, width=1000, height=500)

    # CRIANDO BOTÕES PARA DOWNLOAD
    st_col1_download, st_col2_download = st.columns(2)

    # with st_col1_download:
    #     st.download_button(
    #         label="Download dados (excel)",
    #         data=df_footprint,
    #         file_name="FOOTPRINT_DATA.xlsx",
    #         mime="application/vnd.ms-excel",
    #     )
    #
    # with st_col2_download:
    #     st.download_button(
    #         label="Download mapa",
    #         data=mapobj,
    #         file_name="FOOTPRINT.html",
    #         mime="text/html",
    #     )
