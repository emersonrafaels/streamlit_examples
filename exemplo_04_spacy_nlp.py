import streamlit as st
from streamlit.components import v1 as components
from spacy import load, displacy

def get_spacy_model(language="portuguese"):

    """

        INICIA O MODELO SPACY COM BASE NA LINGUAGEM DEFINIDA.

        # Arguments

        # Returns
            validador                       - Required : Validação da função (Boolean)
            pln                             - Required : Modelo spacy (Spacy)

    """

    # INICIANDO O VALIDADOR
    validador = False

    # INICIANDO O MODELO DO SPACY
    pln = None

    # OBTENDO O MODELO
    if language == "portuguese":
        pln = load('pt_core_news_lg')
        validador = True
    elif language == "english":
        pln = load('en_core_news_lg')
        validador = True

    return validador, pln

# NO WIDGET MAIN, INSERINDO UM TITLE
st.title("APP - SEU MODELO SPACY PT-BR NA VERSÃO WEB")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {
              visibility: hidden;
            }
            footer:after {
              content:'Feito com 🖤 por Emerson Rafael - Github: emersonrafaels'; 
              visibility: visible;
              display: block;
              position: relative;
              #background-color: red;
              padding: 5px;
              top: 2px;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# INICIANDO A SIDEBAR
bar = st.sidebar

# NA SIDEBAR, INSERINDO UM SELECT BOX
choice_selectbox = bar.selectbox(
    'Escolha uma categoria',
    ['Entidades', 'Gramática']
)

# NO WIDGET MAIN, INSERINDO UMA TEXT AREA
text = st.text_area('Insira seu texto, para análise pelo modelo de NLP do Spacy')

# CARREGANDO O MODELO DO SPACY
validator, nlp = get_spacy_model()

# OBTENDO A LISTA DE TAGS DO SPACY
tagger = nlp.get_pipe("morphologizer")
options_tag = [value.split("POS=")[-1] for value in tagger.labels if value.find("|")==-1]
# INSERINDO UMA OPÇÃO DE TODAS
options_tag.insert(0, "TODAS")

if validator:

  doc = nlp(text)

  if text and choice_selectbox == 'Entidades':

    # OBTENDO AS ENTIDADES - USANDO DISPLAY DO SPACY
    data = displacy.render(doc, style='ent')

    # VISUALIZANDO COM O EXPANDER
    with st.expander('Dados do spaCy'):
        components.html(
            data, scrolling=True, height=300
        )

    # DIVIDINDO EM DUAS COLUNAS
    column_one, column_two = st.columns(2)
    for ent in doc.ents:

        column_one.info(ent)
        column_two.warning(ent.label_)

  if text and choice_selectbox == 'Gramática':

    # CRIANDO UM MULTISELECT DE TAGS POSSÍVEIS PARA SELECT
    list_tags_filter = bar.multiselect("Escolha as tags desejadas", 
                                       options=options_tag, 
                                       default=options_tag[0])

    # VISUALIZANDO COM O EXPANDER
    with st.expander('Dados do spaCy'):
          st.json(doc.to_json())    

    # CRIANDO TRÊS COLUNAS
    column_grammar_one, column_grammar_two, column_grammar_three = st.columns(3)

    # INSERINDO OS TÍTULOS DE CADA COLUNA
    column_grammar_one.subheader('Token')
    column_grammar_two.subheader('Tag')
    column_grammar_three.subheader('Morph')

    # PERCORRENDO A ANÁLISE DO TEXTO
    for text in doc:

      # VERIFICANDO SE A TAG ENCONTRA-SE NA LISTA DO MULTISELECT
      if text.tag_ in list_tags_filter or "TODAS" in list_tags_filter:

        # CRIANDO UM CONTAINER
        container = st.container()

        # RECRIANDO AS TRÊS COLUNAS
        # DENTRO DO CONTAINER
        column_grammar_one, column_grammar_two, column_grammar_three = container.columns(3)

        column_grammar_one.info(text)
        column_grammar_two.warning(text.tag_)
        column_grammar_three.error(text.morph)

        # INSERINDO UM HORIZONTAL LINE
        st.markdown("""<hr style="height:1px;border:none;color:#ccccff;background-color:#ccccff;" /> """, 
                    unsafe_allow_html=True)

else:
  st.error("Realize o download do modelo de NLP em Português do Spacy em: https://github.com/explosion/spacy-models/releases/tag/pt_core_news_lg-3.4.0")