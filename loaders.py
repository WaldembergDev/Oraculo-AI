from langchain.document_loaders import WebBaseLoader, YoutubeLoader, CSVLoader, PyPDFLoader, TextLoader
from fake_useragent import UserAgent
import os
import time
import streamlit as st

def carrega_site(url):
    documento = ''
    for i in range(3):
        try:
            os.environ['USER_AGENT'] = UserAgent().random
            loader = WebBaseLoader(url, raise_for_status=True)
            lista_documentos = loader.load()
            documento = '\n'.join([doc.page_content for doc in lista_documentos])
            break
        except:
            print(f'Erro ao carregar o site {i+1}')
            time.sleep(3)
    if documento == '':
        st.error('Não foi possível carregar o site')
        st.stop()
    return documento

def carrega_youtube(id_url_youtube):
    loader = YoutubeLoader(id_url_youtube, add_video_info=False, language=['pt'])
    lista_documentos = loader.load()
    documento = '\n'.join([doc.page_content for doc in lista_documentos])
    return documento

def carrega_csv(caminho_csv):
    loader = CSVLoader(caminho_csv)
    lista_documentos = loader.load()
    documento = '\n'.join([doc.page_content for doc in lista_documentos])
    return documento

def carrega_pdf(caminho_pdf):
    loader = PyPDFLoader(caminho_pdf)
    lista_documentos = loader.load()
    documento = '\n'.join([doc.page_content for doc in lista_documentos])
    return documento

def carrega_txt(caminho_txt):
    loader = TextLoader(caminho_txt)
    lista_documentos = loader.load()
    documento = '\n'.join([doc.page_content for doc in lista_documentos])
    return documento
