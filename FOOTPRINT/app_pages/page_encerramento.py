import pandas as pd
import streamlit as st
from dynaconf import settings
from streamlit_folium import st_folium

from utils.pandas_functions import (
    load_data,
    convert_dataframe_to_aggrid,
    get_indicators_before_versus_after,
    filter_columns_multiselect,
)


def load_encerramento():

    # CARREGANDO DATAFRAME
    df_footprint = load_data(data_dir=settings.DATA_DIR_AGENCIAS)

    # INCLUINDO O DATAFRAME EM TELA
    st.markdown("### Análise de encerramento")
    st.markdown("#### Selecione as agências que você deseja analisar")
    dataframe_aggrid_encerramento = convert_dataframe_to_aggrid(
        data=df_footprint, validator_all_rows_selected=False
    )

    # OBTENDO O DATAFRAME DAS LINHAS SELECIONADAS
    selected_df_encerramento = pd.DataFrame(
        dataframe_aggrid_encerramento["selected_rows"]
    )

    if not selected_df_encerramento.empty:
        selected_df_encerramento = selected_df_encerramento[df_footprint.columns]

        st.markdown("### Agências selecionadas")
        st.dataframe(selected_df_encerramento)

        st.markdown("### Faça upload do arquivo de simulação de encerramento")
        uploaded_file = st.file_uploader(
            "Escolha o arquivo",
            type=["csv", "xlsx"],
            help="O arquivo deve conter as agências selecionadas, caso contrário, não será possível realizar a comparação",
        )
        if uploaded_file is not None:
            st.success("UPLOAD REALIZADO COM SUCESSO")

            # INICIALIZANDO O DATAFRAME QUE RECEBERÁ O RESULTADO
            df_upload = pd.DataFrame()

            # COM ARQUIVO INSERIDO, OBTENDO O TIPO DE ARQUIVO
            print("TIPO DO ARQUIVO: {}".format(uploaded_file.type))

            st.markdown("### Dados carregados")
            if type in ["csv"]:
                df_upload = pd.read_csv(uploaded_file)
            else:
                df_upload = pd.read_excel(uploaded_file)

            st.dataframe(df_upload)

            # REALIZANDO O JOIN ENTRE OS DADOS
            df_join_df1_df2 = get_indicators_before_versus_after(
                df1=selected_df_encerramento, df2=df_upload
            )

            st.markdown("### Comparando as agências")
            multiselect_columns = st.multiselect(
                label="Selecione as colunas desejadas para o estudo de encerramento",
                options=selected_df_encerramento.columns,
                default=None,
                key=None,
                help="O filtro de colunas será aplicado nos dados abaixo",
                on_change=None,
                args=None,
                kwargs=None,
                disabled=False,
                label_visibility="visible",
            )

            if multiselect_columns:
                multiselect_columns_result = filter_columns_multiselect(
                    colunas_desejadas=multiselect_columns,
                    df_columns=df_join_df1_df2.columns,
                )

                # FILTRANDO AS COLUNAS DESEJADAS NO DATAFRAME DE CRUZAMENTO
                df_join_df1_df2 = df_join_df1_df2[multiselect_columns_result]

            df_join_df1_df2_explorer = st.dataframe(data=df_join_df1_df2)
