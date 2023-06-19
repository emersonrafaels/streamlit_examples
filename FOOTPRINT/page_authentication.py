import base64
import yaml
from time import sleep
from pathlib import Path
from yaml.loader import SafeLoader

import streamlit as st
from dynaconf import settings

import utils.authenticator as stauth
from app import main as main_app

def get_credentials():

    # OBTENDO CREDENCIAIS
    with open(settings.PAGE_AUTHENTICATION) as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    return authenticator


# OBTENDO AS CREDENCIAIS
authenticator = get_credentials()

# OBTENDO O DIRETÓRIO DO LOGO
dir_logo = str(Path(Path(__file__).absolute().parent, settings.LOGO_APP))
# CODIFICANDO A IMAGEM EM BASE64
dir_logo = base64.b64encode(open(dir_logo, 'rb').read())

# CRIANDO O WIDGET
name, authentication_status, username = authenticator.login(form_name='Footprint - Autosserviços',
                                                            location='main',
                                                            form_name_username='Usuário',
                                                            form_name_password='Senha',
                                                            form_name_button='Entrar',
                                                            validator_insert_image=True,
                                                            image=dir_logo,
                                                            width_image=100,
                                                            location_image='main',
                                                            position_image='center')

print(name, authentication_status, username, sep="-")

# VERIFICANDO O LOGIN
if authentication_status:
    # st.success("Login realizado com sucesso")
    # sleep(2)
    main_app(authenticator)
elif username in [None, ""] and authentication_status is False:
    st.warning('Por favor, inserir usuário e senha')
elif authentication_status is False:
    st.error('Usuário ou senha estão incorretos')
elif authentication_status is None:
    st.warning('Por favor, inserir usuário e senha')
