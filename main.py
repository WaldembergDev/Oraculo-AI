import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from loaders import carrega_csv, carrega_pdf, carrega_site, carrega_txt, carrega_youtube
from langchain.prompts import ChatPromptTemplate
import tempfile


TIPOS_ARQUIVOS_VALIDOS = [
    'Site',
    'Youtube',
    'PDF',
    'CSV',
    'TXT'
]

CONFIG_MODELOS = {
    'Groq': {'Modelos': ['llama-3.3-70b-versatile', 'gemma2-9b-it'],
             'chat': ChatGroq},
    'OpenAI': {'Modelos': ['gpt-4o-mini', 'gpt-4.1', 'gpt-4o', 'o1-mini'],
               'chat': ChatOpenAI}
}

MEMORIA = ConversationBufferMemory()

def carrega_arquivo(tipo_arquivo, arquivo):
    if tipo_arquivo == 'Site':
        documento = carrega_site(arquivo)
    if tipo_arquivo == 'Youtube':
        documento = carrega_youtube(arquivo)
    if tipo_arquivo == 'PDF':
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carrega_pdf(nome_temp)
    if tipo_arquivo == 'CSV':
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carrega_csv(nome_temp)
    if tipo_arquivo == 'TXT':
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carrega_txt(nome_temp)
    return documento


def carrega_modelo(provedor, modelo, api_key, tipo_arquivo, arquivo):      
    documento = carrega_arquivo(tipo_arquivo, arquivo)

    system_message = '''Você é um assistente amigável chamado Oráculo. Você possui acesso às seguintes informações vindas de um documento {}:

    ####
    {}
    ####

    Utilize as informações fornecidas para basear as suas respostas e dados apenas referente ao documento. Perguntas não relacionadas ao documento informe que não pode passar a informação.

    Sempre que houver $ na sua saída, substitua por S.

    Se a informação do documento for algo como "Just a moment... Enable Javascript and cookies to continue" sugira ao usuário carregar novamente o Oráculo!
    '''.format(tipo_arquivo, documento)

    template = ChatPromptTemplate.from_messages([
        ('system', system_message),
        ('placeholder', '{chat_history}'),
        ('user', '{input}')
    ])

    chat = CONFIG_MODELOS[provedor].get('chat')(model=modelo, api_key=api_key)
    chain = template | chat
    st.session_state['chain'] = chain


def pagina_chat():
    st.header('Bem vindo ao oráculo!', divider=True)
    chain = st.session_state.get('chain')
    if chain is None:
        st.error('Carregue o Oráculo')
        st.stop()

    memoria = st.session_state.get('memoria', MEMORIA)
    for mensagem in memoria.buffer_as_messages:
        chat = st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)
    input_usuario = st.chat_input('Fale com o oráculo')
    if input_usuario:
        chat = st.chat_message('human')
        chat.markdown(input_usuario)

        chat = st.chat_message('ai')
        resposta = chat.write_stream(chain.stream({
            'input': input_usuario,
            'chat_history': memoria.buffer_as_messages
            }))
        # adicionando o input do usuário nas mensagens
        memoria.chat_memory.add_user_message(input_usuario)        
        memoria.chat_memory.add_ai_message(resposta)
        # armazenando as mensagens na sessão do usuário
        st.session_state.memoria = memoria

def sidebar():
    tabs = st.tabs(['Upload de arquivos', 'Seleção de modelos'])
    with tabs[0]:
        tipo_arquivo = st.selectbox('Selecione o tipo de arquivo', TIPOS_ARQUIVOS_VALIDOS)
        if tipo_arquivo == 'Site':
            arquivo = st.text_input('Digite a url do site')
        if tipo_arquivo == 'Youtube':
            arquivo = st.text_input('Digite a url do vídeo')
        if tipo_arquivo == 'PDF':
            arquivo = st.file_uploader('Selecione o PDF', type=['.pdf'])
        if tipo_arquivo == 'CSV':
            arquivo = st.file_uploader('Selecione o arquivo CSV', type=['.csv'])
        if tipo_arquivo == 'TXT':
            arquivo = st.file_uploader('Selecione o arquivo TXT', type=['.txt'])
    
    with tabs[1]:
        provedor = st.selectbox('Selecione o profedor dos modelos', CONFIG_MODELOS.keys())
        modelo = st.selectbox('Selecione o modelo', CONFIG_MODELOS[provedor].get('Modelos'))
        api_key = st.text_input(f'Adicione a API_KEY para o provedor {provedor}', value=st.session_state.get(f'api_key_{provedor}'))
        st.session_state[f'api_key_{provedor}'] = api_key
    
    if st.button('Inicializar oráculo'):
        carrega_modelo(provedor, modelo, api_key, tipo_arquivo, arquivo)
    if st.button('Apagar histórico de conversa'):
        st.session_state['memoria'] = MEMORIA


def main():
    with st.sidebar:
        sidebar()
    pagina_chat()

if __name__ == '__main__':
    main()