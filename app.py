import streamlit as st
from textblob import TextBlob


st.title("Chat de Análise de Sentimentos", text_alignment="center")
user_input = st.chat_input("Digite sua mensagem para análise:")


st.sidebar.title("Configuração")
response_type = st.sidebar.checkbox("Mostra resposta em JSON", value=True)
model = st.sidebar.selectbox("Modelos disponíveis", ["TextBlob", "oracleModel"])
user_name = st.sidebar.text_input("Nome do Usuário", value="você").capitalize().strip()
user_icon = st.sidebar.file_uploader("Enviar ícone do usuário", type=['jpg','png','jpeg'])


if user_icon is not None:
    st.sidebar.image(user_icon)

def responseJson(sentiment, acc):
    return {
        "previsibilidade": sentiment,
        "probabilidade": f"{acc:.2f}"
    }

def responseAlternative(sentiment, acc):
    if acc > 0:
        st.success(f"{sentiment} - Probabilidade: {acc:.2f}")
    elif acc < 0:
        st.error(f"{sentiment} - Probabilidade: {acc:.2f}")
    else:
        st.warning(f"{sentiment} - Probabilidade: {acc:.2f}")
        

@st.cache_data
def analyze(text: str):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    
    if sentiment > 0:
        return responseJson("Positivo", sentiment)
    elif sentiment < 0:
        return responseJson("Negativo", sentiment)
    else:
        return responseJson("Neutro", sentiment)

def list_analyses():
    st.sidebar.subheader("Histórico")
    for name, user_text, result, user_icon in st.session_state.history:
        st.sidebar.write(f"{name}: {user_text}")
        st.sidebar.json(result)

if "history" not in st.session_state:
    st.session_state.history = []

if user_input:
    try:
        result = analyze(user_input)
        st.session_state.history.append((user_name, user_input, result, user_icon))
    except Exception as e:
        st.chat_message("assistant").error(f"Ocorreu um erro: {e}")

for name, user_text, result, icon in st.session_state.history:
    with st.chat_message("user", avatar=icon if icon is not None else None):
        st.markdown(
            f"""
            <style>
                .user-msg {{
                    text-align: right;
                }}
            </style>
            <p class="user-msg">{name}: {user_text}</p>
            """,
            unsafe_allow_html=True
        )

    with st.chat_message("assistant"):
        if response_type:
            st.json(result)
        else:
            responseAlternative(result["previsibilidade"], float(result["probabilidade"]))

list_analyses()
