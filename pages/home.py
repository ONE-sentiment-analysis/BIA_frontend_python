#Parte Principal do projeto

import streamlit as st
from textblob import TextBlob
from streamlit_option_menu import option_menu
import requests

#Título da página (visível na aba)
st.set_page_config(page_title="BIA • Home", layout="wide")


st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
.nav-container {
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

#Caso o usuário tente entrar sem login 
if "logado" not in st.session_state or not st.session_state.logado:
    st.info("Por favor, faça login primeiro.")
    st.switch_page("index.py") #página de login

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "sobre"

if "history" not in st.session_state:
    st.session_state.history = []


tab_map = {"sobre": 0, "analise": 1, "hist": 2}
current_index = tab_map.get(st.session_state.active_tab, 0)

# Navbar para navegação entre os "setores" + css
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
selected = option_menu(
    menu_title=None,
    options=["Sobre", "Análise de Sentimentos", "Histórico"],
    icons=["bi-info-circle", "bi-cpu", "bi-clock-history"],
    default_index=current_index,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "0px!important", 
            "background-color": "#590F7F",
            "border-radius": "10px",
            "display": "flex",
            "justify-content": "center",
            "overflow": "hidden"
        },
        "icon": {
            "color": "white", 
            "font-size": "16px"
        }, 
        "nav-link": {
            "flex": "1",
            "display": "flex",
            "align-items": "center",
            "justify-content": "center",
            "gap": "8px",
            "font-size": "14px", 
            "color": "white",
            "text-align": "center", 
            "margin": "0px", 
            "padding": "15px 5px",
            "font-weight": "500",
            "border-right": "1px solid rgba(255, 255, 255, 0.15)",
            "border-radius": "0px",
            "--hover-color": "#410B5D",
            "white-space": "nowrap"
        },
        "nav-link-selected": {
            "background-color": "#3C0A55", 
            "font-weight": "bold",
        },
    }
)

# Atualização de estado baseada na seleção
if selected == "Sobre" and st.session_state.active_tab != "sobre":
    st.session_state.active_tab = "sobre"
    st.rerun()
elif selected == "Análise de Sentimentos" and st.session_state.active_tab != "analise":
    st.session_state.active_tab = "analise"
    st.rerun()
elif selected == "Histórico" and st.session_state.active_tab != "hist":
    st.session_state.active_tab = "hist"
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Define a variável de controle baseada no estado
active = st.session_state.active_tab

st.divider()

# Configuração da Aba "Sobre" onde explica um pouco do projeto + Tecnologias utilizadas
if active == "sobre":
    st.markdown("## 🤖 B.I.A — Assistente de Análise de Sentimentos")
    texto = ("Projeto desenvolvido como estrutura base para o Hackaton da ORACLE."
    " Esta aplicação, construída com Spring Boot, tem como objetivo integrar-se a um modelo de classificação de sentimentos fornecido por uma API externa desenvolvida em Python."
    "O sistema envia textos para o modelo de Machine Learning, recebe a análise de sentimento (como positivo, negativo ou neutro) e retorna o resultado estruturado para o cliente."
    "Essa arquitetura permite que o backend Java funcione como intermediário entre o usuário e o modelo de IA, garantindo organização, segurança e escalabilidade.")
    st.markdown(f'<div style="text-align: justify;">{texto}</div>', unsafe_allow_html=True)
    st.write("")
    
    st.markdown("### 💻 Tecnologias utilizadas")
    st.markdown("- Java 17+ \n- Spring Boot 2.5+ \n- Spring Web \n- DevTools \n- Lombok \n- HttpClient (Java 11+) \n- Jackson (ObjectMapper) \n- JUnit + Mockito + H2 \n- Resilience4j (Circuit Breaker, Retry, Rate Limiter, Bulkhead, TimeLimiter)  \n- Observabilidade: Actuator + Prometheus + Grafana \n- Dockerfile e docker-compose")


# Análise dos sentimentos - Parte principal onde a B.I.A conversa com os usários 

elif active == "analise":
    
    st.sidebar.title("Configuração")
    response_type = st.sidebar.checkbox("Mostrar resposta em JSON", value=True)
    model_choice = st.sidebar.selectbox("Modelo", ["TextBlob", "Oracle"])
    user_name = st.sidebar.text_input("Nome do usuário", value="você").capitalize().strip()
    ia_name = "BIA"
    col_titulo, col_foto = st.columns([0.85, 0.15])
    with col_titulo:
        st.title('🤖 Análise de Sentimentos', help='https://github.com/ONE-sentiment-analysis/BIA_frontend_python')
    
    #Botão para upload de fotos e prévia da mesma
    with col_foto:
        with st.popover("Foto"):
            st.write("Ajuste seu Perfil")
            user_icon = st.file_uploader("Escolha uma foto", type=["jpeg", "jpg", "png"])
            if user_icon is not None: #Caso não esteja vazio
                st.image(user_icon, caption="Prévia da foto", width=150)
    
    user_input = st.chat_input("Digite sua mensagem para análise:")

    # Funções para análise dos sentimento enviados pelo usuário
    def responseJson(sentiment, acc):
        return {"previsibilidade": sentiment, "probabilidade": round(acc, 2)}

    def responseAlternative(sentiment, acc):
        if acc > 0:
            st.success(f"{sentiment} - Probabilidade: {acc:.2f}")
        elif acc < 0:
            st.error(f"{sentiment} - Probabilidade: {acc:.2f}")
        else:
            st.warning(f"{sentiment} - Probabilidade: {acc:.2f}")
            
    @st.cache_data
    def analyze(text: str, model: str):
        if model == "TextBlob":
            blob = TextBlob(text)
            sentiment = blob.sentiment.polarity  
        else:
            sentiment = 0
            st.warning("Estamos implementando outro modelo")
        
        if sentiment > 0:
            return responseJson("Positivo", sentiment)
        elif sentiment < 0:
            return responseJson("Negativo", sentiment)
        else:
            return responseJson("Neutro", sentiment)

    if user_input:
        result = analyze(user_input, model_choice)
        st.session_state.history.append((user_name, user_input, result, user_icon))

    
    for name, text, result, icon in st.session_state.history:
        with st.chat_message("user", avatar=icon if icon is not None else None):
            st.write(f"**{name}**")
            st.write(text)
            
        with st.chat_message("assistant", avatar="🤖"):
            st.write(f"**{ia_name}**")

            
            if response_type:
                st.json(result)
            else:
                responseAlternative(result["previsibilidade"], result["probabilidade"])



#Página de Histórico, onde fica salvo as análises e perguntas anteriores 
elif active == "hist":
    st.markdown("## 📜 Histórico")
    if not st.session_state.history:
        st.info("Nenhuma análise ainda.")
    else:
        if st.button("Limpar Tudo"): #Botão de Limpeza de Histórico 
            st.session_state.history = []
            st.rerun()
        for i, (name, text, result, icon) in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Análise {len(st.session_state.history)-i}: {text[:30]}..."):
                st.write(f"**Usuário:** {name}")
                st.write(f"**Texto:** {text}")
                st.write(f"**Sentimento:** {result['previsibilidade']}")
                st.write(f"**Probabilidade:** {result['probabilidade']}")