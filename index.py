#Tela "principal e tela de Login (a fazer: conectar o backend)"

import streamlit as st

# ---------- CONFIGURAÇÃO ----------
st.set_page_config(page_title="Login", layout="centered")


st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

#Testes de usuários
USERS = {
    "coiso@coiso.com": {"senha": "1234", "nome": "Gigi"},
    "mail@mail.com": {"senha": "1234", "nome": "Teste"}
}

#sessão
if "logado" not in st.session_state:
    st.session_state.logado = False

if "nome" not in st.session_state:
    st.session_state.nome = ""


#CSS da página
def aplicar_estilo():
      st.markdown("""
        <style>
        
        [data-testid="stForm"] {
            border: 1px solid #333;
            border-radius: 15px;
            background-color: #181621;
            padding: 2rem;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        
        /* Centraliza o título */
        h2 {
            color: #335E91;
            padding-bottom: 10px;
        }

        /* Estiliza o botão de LOGIN  */
        div[data-testid="stFormSubmitButton"] > button:first-child {
            background-color: #590F7F!important;
            color: white !important;
            border-radius: 8px;
            border: none;
            height: 3em;
            font-weight: bold;
            transition: 0.3s;
        }
        
        div[data-testid="stFormSubmitButton"] > button:first-child:hover {
            background-color: #410B5D !important;
            transform: scale(1.02);
        }

        /* Estiliza o botão de CADASTRO  */
        
        div.stColumn:nth-of-type(3) button {
            background-color: transparent !important;
            color:#6F139C !important;
            border: 1px solid #30363d !important;
            border-radius: 8px;
            height: 3em;
            transition: 0.3s;
        }

        div.stColumn:nth-of-type(3) button:hover {
            border-color: #8b949e !important;
            background-color: #21262d !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

#Função do Login 
def tela_login():
    aplicar_estilo()

    with st.form("login_form"):
        st.markdown("<h2 style='text-align:center;'>Login</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:gray;'>Entre com suas credenciais</p>", unsafe_allow_html=True)
        st.divider()
        email = st.text_input("Email",
                              icon=':material/mail:')
        password = st.text_input("Senha", type="password",
                                 icon=':material/lock:')

        st.write("") 

        col_espaco1, col_login, col_cad, col_espaco2 = st.columns([0.8, 1, 1, 0.8]) #Colunas para ajeitar os botões na tela 
        with col_login:
            submitted = st.form_submit_button("Entrar", use_container_width=True)
        
        with col_cad:
            register = st.form_submit_button("Cadastrar", use_container_width=True)


        if submitted:
            if email in USERS and USERS[email]["senha"] == password:
                st.session_state.logado = True
                st.session_state.nome = USERS[email]["nome"]
                st.switch_page("pages/home.py") #Tela principal do programa 
                st.success("Login realizado com sucesso")
            else:
                st.error("Email ou senha inválidos")
        if register:
            st.switch_page("pages/cadastro.py") 

#Caso não esteja logado, ficar nessa mesma página
if not st.session_state.logado:
    tela_login()
