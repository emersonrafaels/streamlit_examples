import streamlit as st
from PIL import Image, ImageFont, ImageDraw


def text_on_image(image, text, font_size, color):

    # REALIZANDO A ABERTURA DA IMAGEM
    img = Image.open(image)

    # REALIZANDO A DEFINIÇÃO DA FONTE
    font = ImageFont.truetype('Caliban-m132.ttf', font_size)

    # INSTANCIANDO O DESENHO SOBRE A IMAGEM
    draw = ImageDraw.Draw(img)

    # OBTENDO O TAMANHO DA IMAGEM
    # IW: LARGURA ; IH: ALTURA
    iw, ih = img.size

    # OBTENDO O TAMANHO DA FONTE
    fw, fh = font.getsize(text)

    # ESCREVENDO SOBRE A IMAGEM - CENTRALIZANDO
    # LARGURA: (LARGURA TOTAL DA IMAGEM - LARGURA DA FONTE)/2
    # ALTURA: (ALTURA TOTAL DA IMAGEM - ALTURA DA FONTE)/2
    draw.text(
        ((iw - fw) / 2, (ih - fh) / 2),
        text,
        fill=color,
        font=font
    )

    # SALVANDO A IMAGEM RESULTANTE
    img.save('last_image.jpg')

st.set_page_config(
        page_title="SEU CRIADOR DE MARCA DE ÁGUA",
        page_icon="chart_with_upwards_trend",
        layout="wide",
    )

st.markdown('''
    ### APP - SEU CRIADOR DE MARCA DE ÁGUA
''')

image = st.file_uploader('Selecione uma imagem', type=['jpg', 'png'])

text = st.text_input('Texto para sua marca dágua')

# color = st.selectbox(
#     'Cor da sua marca', ['black', 'white', 'red', 'green']
# )

color = st.color_picker('Escolha uma cor')

font_size = st.number_input('Tamanho da fonte', min_value=50)

# VERIFICANDO SE UMA IMAGEM FOI INSERIDA
if image:

    # SE INSERIDA UMA IMAGEM
    # BUTTON DISPONÍVEL PARA APLICAR A MARCA DE ÁGUA
    result = st.button(
        'Aplicar',
        type='primary',
        on_click=text_on_image,
        args=(image, text, font_size, color)
    )
    if result:

        # VISUALIZANDO A IMAGEM
        st.image('last_image.jpg')

        # HABILITANDO BOTÃO DE DOWNLOAD
        with open('last_image.jpg', 'rb') as file:
            st.download_button(
                'Baixe agora mesmo sua foto com marca',
                file_name='image_com_marca.jpg',
                data=file,
                mime='image/jpg',
                help="A imagem será baixada com o nome de 'image_com_marca.jpg'"
            )
else:
    st.warning('Ainda não temos imagem!')