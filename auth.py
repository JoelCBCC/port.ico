import streamlit as st
from database import get_users

def login():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>📅 Sistema Kanban</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666;'>Faça login para acessar</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("E-mail")
            password = st.text_input("Senha", type="password")
            
            submitted = st.form_submit_button("Entrar", use_container_width=True)
            if submitted:
                users_df = get_users()
                if not users_df.empty:
                    # Garantir que a coluna password seja tratada como string caso o pandas a leia como int
                    user_row = users_df[(users_df['email'] == email) & (users_df['password'].astype(str) == str(password))]
                    if not user_row.empty:
                        st.session_state['user'] = {
                            'email': user_row.iloc[0]['email'],
                            'profile': user_row.iloc[0]['profile'],
                            'name': user_row.iloc[0]['name']
                        }
                        st.rerun()
                    else:
                        st.error("Credenciais inválidas. Tente novamente.")
                else:
                    st.error("Base de usuários vazia.")

def logout():
    if 'user' in st.session_state:
        del st.session_state['user']
        st.rerun()

def check_auth():
    if 'user' not in st.session_state:
        login()
        return False
    return True
