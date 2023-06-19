import base64
import os
import yaml
from pathlib import Path
from yaml.loader import SafeLoader

import streamlit as st
from dynaconf import settings
from streamlit_custom_notification_box import custom_notification_box

import utils.authenticator as stauth
from app_pages import page_autosservico
from app_pages import page_encerramento
from utils.streamlit_functions import add_logo

# CONFIGURANDO O APP
st.set_page_config(
    page_title="FOOTPRINT - GESTÃO DO PARQUE DE AGÊNCIAS",
    page_icon=":world-map:",
    layout="wide",
)


def main(authenticator):

    if st.session_state.get("authentication_status"):

        # ADICIONANDO TITULO DA PÁGINA
        st.title("APP - FOOTPRINT - GESTÃO DO PARQUE DE AGÊNCIAS")

        # OBTENDO O DIRETÓRIO DO LOGO
        dir_logo = os.path.join(Path(__file__).absolute().parent, settings.LOGO_APP)
        dir_logo = settings.LOGO_APP

        # ADICIONANDO LOGO
        add_logo(dir_logo, width=100, location='sidebar', position_image='left')

        with st.sidebar:
            # ESTUDO DESEJADO
            st.title("Defina o estudo desejado")

            options_estudos = [
                "Autosserviço",
                "Encerramento",
                "Remanejamento",
                "Abertura",
                "Áreas ociosas",
                "Intervenções estratégicas",
            ]

            selected_estudo_desejado = st.radio(
                label="Estudo desejado",
                options=options_estudos,
                index=0,
                key=None,
                help="Escolha o estudo desejado e na página central aparecerá novas opções",
                on_change=None,
                disabled=False,
                horizontal=False,
                label_visibility="visible",
            )

            # CRIANDO UMA LINHA EM BRANCO
            st.divider()

            # INCLUINDO O BOTÃO DE LOGOUT
            authenticator.logout('Sair',
                                 'main',
                                 key='app_page')

        if selected_estudo_desejado == "Autosserviço":
            # CARREGANDO A PÁGINA DE AUTOSSERVIÇO
            page_autosservico.load_autosservico()

        elif selected_estudo_desejado == "Encerramento":
            # CARREGANDO A PÁGINA DE ENCERRAMENTO
            page_encerramento.load_encerramento()

        else:
            st.markdown("### Feature em desenvolvimento")

            styles = {
                "material-icons": {"color": "black"},
                "text-icon-link-close-container": {"box-shadow": "#3896de 0px 4px"},
                "notification-text": {"": ""},
                "close-button": {"": ""},
                "link": {"": ""},
            }

            custom_notification_box(
                icon="view_kanban",
                textDisplay="Essa página está em construção",
                externalLink="",
                url="#",
                styles=styles,
                key="notification_desenv",
            )

if __name__ == "__main__":
    main()
