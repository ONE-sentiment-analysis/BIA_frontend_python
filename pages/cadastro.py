#Tela de cadastro 


import streamlit as st
import requests

def login(password: str, email: str):
    urlAPI = 'http:localhost:8080/api/v1/auth'
    userData = {
        f"email": {email},
        f"nome": {password}
    }
    
    try:
        response = requests.post(url=urlAPI, json=userData)
        if (response.status_code == 201): #201 status criado
            # st.success(f'Login realizado com sucesso. Bem-vindo {name.capitalize()}')
            st.success(f'Login realizado com sucesso.')
        else:
            st.error(f'Erro ao realizar login {response.status_code}')
            st.write(response.text)
    except Exception as e:
        st.error(f'Ocorreu um erro {e}')


def registerUser(name: str, email:str, password:str):
    urlAPI = 'http:localhost:8080/api/v1/auth'
    newUser = {
        "name": {name},
        "email": {email},
        "password": {password}
    }
    
    try:
        response = requests.post(url=urlAPI, json=newUser)
        if (response.status_code == 201): # TODO: adicionar mais tratamentos de erro para status code
            st.success(f'Usuário criado com sucesso')
        else:
            st.warning(f'Erro ao criar usuário')
    except Exception as e:
        st.warning(f'Ocorreu um erro {e}')


#Título da página (visível na aba)
st.set_page_config(page_title="Cadastro", layout="centered")


st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

#CSS da página
def aplicar_estilo():
    st.markdown("""
    <style>

    /* CARD */
    [data-testid="stForm"] {
        border: 1px solid #333;
        border-radius: 18px;
        background-color: #181621;
        padding: 2.5rem;
        box-shadow: 0 6px 18px rgba(0,0,0,0.45);
        max-width: 520px;
        margin: auto;
    }

    h2 {
        color: #335E91;
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }

    /* BOTÕES - BASE */
    div[data-testid="stFormSubmitButton"] button {
        height: 3.8em;
        font-size: 1.05rem;
        font-weight: 600;
        border-radius: 12px;
        transition: all 0.25s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }

    /* BOTÃO 1 — CADASTRAR */
    div[data-testid="stFormSubmitButton"] button:nth-of-type(1) {
        background-color: #590F7F !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(65, 11, 93, 1.0);
    }

    div[data-testid="stFormSubmitButton"] button:nth-of-type(1):hover {
        background-color: #410B5D !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(65, 11, 93, 1.0);
    }

    /* BOTÃO 2 — VOLTAR */
    div[data-testid="stFormSubmitButton"] button:nth-of-type(2) {
        background-color: transparent !important;
        color: #590F7F !important;
        border: 1px solid #30363d !important;
    }

    div[data-testid="stFormSubmitButton"] button:nth-of-type(2):hover {
        border-color: #410B5D !important;
        background-color: #21262d !important;
        color: white !important;
        transform: translateY(-2px);
    }

    </style>
    """, unsafe_allow_html=True)

#Formulário de cadastro
aplicar_estilo()

with st.form("cadastro_form"):
    st.markdown("<h2 style='text-align:center;'>Cadastro</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; color:gray;'>Seja bem-vindo(a)! Faça seu cadastro aqui.</p>",
        unsafe_allow_html=True
    )
    st.divider()

    nome = st.text_input("Nome", icon=":material/person:")
    email = st.text_input("Email", icon=":material/mail:")
    senha = st.text_input("Senha", type="password", icon=":material/lock:")
    
    
    registerUser(name=nome, email=email, password=senha)
    
    
    st.selectbox(
        "Selecione seu pronome:",
        [
            "Ele/Dele",
            "Ela/Dela",
            "Elu/Delu (neutro)",
            "Outro",
            "Prefiro não informar"
        ]
    )

    st.write("")

    col_espaco1, col_cadastrar, col_voltar, col_espaco2 = st.columns([0.6, 1.4, 1.4, 0.6]) #Coluna para espaçamento e posição dos botões

    with col_cadastrar:
        cadastrar = st.form_submit_button("Cadastrar", use_container_width=True)

    with col_voltar:
        voltar = st.form_submit_button("↩ Voltar", use_container_width=True)


if cadastrar:
    if not nome or not email or not senha:
        st.error("Preencha todos os campos")
    else:
        st.success("Usuário cadastrado com sucesso 🎉")
        st.switch_page("index.py")

if voltar:
    st.switch_page("index.py")
