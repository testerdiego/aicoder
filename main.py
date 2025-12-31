# Importa módulo para interagir com o sistema operacional
import os

# Importa a biblioteca Streamlit para criar a interface web interativa
import streamlit as st

# Importa a classe Groq para se conectar à API da plataforma Groq e acessar o LLM
# from groq import Groq

# Link das pastas
from agents.programming import build_programming_prompt
from services.groq_client import get_groq_client

# Configura a página do Streamlit com título, ícone, layout e estado inicial da sidebar
st.set_page_config(
    page_title="AI Coder",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cria o conteúdo da barra lateral no Streamlit
with st.sidebar:
    
    # Define o título da barra lateral
    st.title("🤖 AI Coder")
    
    # Mostra um texto explicativo sobre o assistente
    st.markdown("Um assistente de IA focado em programação para ajudar iniciantes.")

    linguagem = st.selectbox(
        "Selecione a linguagem:",
        ["Python 🐍", "C# 🎵", "JavaScript ✨", "Java ☕"]
    )

        # Extrai nome puro da linguagem (sem emoji)
    linguagem_pura = linguagem.rsplit(" ", 1)[0]
    
    # Campo para inserir a chave de API da Groq
    # groq_api_key = os.getenv("GROQ_API_KEY")

    # Adiciona linhas divisórias e explicações extras na barra lateral
    st.markdown("---")
    st.markdown("IA pode cometer erros. Sempre verifique as respostas.")

    # st.markdown("---")
    # st.markdown("Estamos em teste")

    # Link para o site
    st.markdown("🔗 Site em breve")
    
    # Botão de link para enviar e-mail ao suporte
    st.link_button("✉️ E-mail Para o Suporte no Caso de Dúvidas", "mailto:EMAIL")

# Título principal do app
# st.title("AI Coder")

# Subtítulo adicional
st.title(f"Assistente Pessoal de Programação {linguagem.split()[1]}")

# Texto auxiliar abaixo do título
st.caption(f"Faça sua pergunta sobre a linguagem {linguagem_pura} e obtenha código, explicações e referências.")

# Inicializa o histórico de mensagens na sessão, caso ainda não exista
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe todas as mensagens anteriores armazenadas no estado da sessão
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Inicializa a variável do cliente Groq como None
try:
    client = get_groq_client()

# Verifica se o usuário forneceu a chave de API da Groq
except Exception as e:
    # Exibe erro caso haja problema ao inicializar cliente
        st.sidebar.error(f"Erro ao inicializar o cliente Groq: {e}")
        st.stop()

# Captura a entrada do usuário no chat
if prompt := st.chat_input(f"Qual sua dúvida sobre {linguagem_pura}"):
    
    # Se não houver cliente válido, mostra aviso e para a execução
    if not client:
        st.warning("API não configurada. Contate o administrador do sistema.")
        st.stop()

    # Armazena a mensagem do usuário no estado da sessão
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Exibe a mensagem do usuário no chat
    with st.chat_message("user"):
        st.markdown(prompt)

# Monta prompt do sistema dinamicamente
    system_prompt = build_programming_prompt(linguagem_pura)
    messages_for_api = [{"role": "system", "content": system_prompt}]
    messages_for_api += st.session_state.messages

    # Cria a resposta do assistente no chat
    with st.chat_message("assistant"):
        
        with st.spinner("Analisando sua pergunta..."):
            
            try:
                
                # Chama a API da Groq para gerar a resposta do assistente
                chat_completion = client.chat.completions.create(
                    messages = messages_for_api,
                    model = "openai/gpt-oss-120b", 
                    temperature = 0.7,
                    max_tokens = 2048,
                )
                
                # Extrai a resposta gerada pela API
                ai_resposta = chat_completion.choices[0].message.content
                
                # Exibe a resposta no Streamlit
                st.markdown(ai_resposta)
                
                # Armazena resposta do assistente no estado da sessão
                st.session_state.messages.append({"role": "assistant", "content": ai_resposta})

            # Caso ocorra erro na comunicação com a API, exibe mensagem de erro
            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com a API da Groq: {e}")

# st.markdown(
#     """
#     <div style="text-align: center; color: gray;">
#         <hr>
#         <p>Hello World</p>
#     </div>
#     """,
#     unsafe_allow_html=True
# )




