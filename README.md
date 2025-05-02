# Oráculo AI

Oráculo AI é um assistente interativo desenvolvido com Streamlit que utiliza modelos de linguagem avançados para responder perguntas com base em documentos fornecidos pelo usuário. Ele suporta múltiplos formatos de entrada, como sites, vídeos do YouTube, PDFs, arquivos CSV e TXT.

## Funcionalidades

- **Upload de Arquivos**: Carregue documentos nos formatos suportados para análise.
- **Modelos de Linguagem**: Configure e utilize modelos de provedores como OpenAI e Groq.
- **Histórico de Conversas**: Mantenha um histórico das interações para uma experiência contínua.
- **Interface Intuitiva**: Interface amigável para upload de arquivos e seleção de modelos.

## Tecnologias Utilizadas

- **Streamlit**: Framework para criação de interfaces web interativas.
- **LangChain**: Biblioteca para construção de pipelines de processamento de linguagem natural.
- **Modelos de Linguagem**: Integração com OpenAI e Groq.

## Como Usar

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/projeto-oraculo.git
   cd projeto-oraculo
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o aplicativo:
   ```bash
   streamlit run main.py
   ```

4. Acesse a aplicação no navegador em `http://localhost:8501`.

## Configuração

- **Upload de Arquivos**: Selecione o tipo de arquivo (Site, YouTube, PDF, CSV ou TXT) e carregue o documento.
- **Seleção de Modelos**: Escolha o provedor (OpenAI ou Groq), o modelo desejado e insira a API Key correspondente.