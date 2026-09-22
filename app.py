import streamlit as st
import pandas as pd
import subprocess
from auth import check_auth, logout
from database import get_visible_cards, get_directors, add_director, remove_director, update_director, get_rooms, add_room, remove_room, update_room, get_users, add_user, remove_user, get_services, add_service, remove_service, update_service, get_directors_dict, get_rooms_dict, get_services_dict
from models import CATEGORIES
from components import render_card, create_card_modal

COLORS = ["green", "light_green", "purple", "lilac", "red", "brown", "blue", "yellow", "gray"]

@st.dialog("Sobre o Port.Ico", width="large")
def about_modal():
    tab_about, tab_changelog = st.tabs(["Sobre", "Change Log"])
    
    with tab_about:
        st.markdown("<h2 style='text-align: center;'>📅 Port.Ico</h2>", unsafe_allow_html=True)
        st.write("**Desenvolvedora:** Thais Lopes")
        
        try:
            last_commit_date = subprocess.check_output(['git', 'log', '-1', '--format=%cd']).decode('utf-8').strip()
            last_commit_hash = subprocess.check_output(['git', 'log', '-1', '--format=%h']).decode('utf-8').strip()
        except Exception:
            last_commit_date = "N/A"
            last_commit_hash = "N/A"
            
        st.write(f"**Versão (Commit):** {last_commit_hash}")
        st.write(f"**Última Atualização:** {last_commit_date}")
        
    with tab_changelog:
        try:
            import os
            changelog_path = os.path.join(os.path.dirname(__file__), "CHANGELOG.md")
            if os.path.exists(changelog_path):
                with open(changelog_path, "r", encoding="utf-8") as f:
                    st.markdown(f.read())
            else:
                st.info("Nenhum registro de mudança encontrado.")
        except Exception as e:
            st.error("Não foi possível carregar o Change Log.")
            
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Fechar", use_container_width=True):
        st.rerun()

@st.dialog("Editar Diretor")
def edit_director_modal(old_name, old_color):
    new_name = st.text_input("Novo nome para o diretor", value=old_name)
    new_color = st.selectbox("Cor da Etiqueta", COLORS, index=COLORS.index(old_color) if old_color in COLORS else 0)
    if st.button("Salvar Alteração", type="primary"):
        update_director(old_name, new_name, new_color)
        st.rerun()

@st.dialog("Editar Sala")
def edit_room_modal(old_name, old_color):
    new_name = st.text_input("Novo nome para a sala", value=old_name)
    new_color = st.selectbox("Cor da Etiqueta", COLORS, index=COLORS.index(old_color) if old_color in COLORS else 0)
    if st.button("Salvar Alteração", type="primary"):
        update_room(old_name, new_name, new_color)
        st.rerun()

@st.dialog("Editar Serviço")
def edit_service_modal(old_name, old_color):
    new_name = st.text_input("Novo nome para o serviço", value=old_name)
    new_color = st.selectbox("Cor da Etiqueta", COLORS, index=COLORS.index(old_color) if old_color in COLORS else 0)
    if st.button("Salvar Alteração", type="primary"):
        update_service(old_name, new_name, new_color)
        st.rerun()

# Configuração da página
st.set_page_config(
    page_title="Port.Ico",
    page_icon="📅",
    layout="wide"
)

# Estilização básica para simular o fundo do Kanban
st.markdown("""
    <style>
    div[data-testid="column"] {
        background-color: #ebecf0;
        padding: 10px;
        border-radius: 8px;
        min-height: 80vh;
    }
    </style>
""", unsafe_allow_html=True)

@st.fragment(run_every=10)
def render_kanban_board(user):
    # Adicionar cartão
    if user['profile'] in ['Presidência', 'Pool']:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕  Adicionar Novo Agendamento", type="primary"):
            create_card_modal(user['email'], user['profile'])
        st.markdown("<br>", unsafe_allow_html=True)
            
    # Carregar dados visíveis
    df_all = get_visible_cards(user['profile'], user['email'])
    df = df_all[df_all['status'] != 'concluido'] if not df_all.empty and 'status' in df_all.columns else df_all
    
    # Se houver dados, ordenar por due_date (crescente)
    if not df.empty:
        df['due_date_dt'] = pd.to_datetime(df['due_date'])
        df = df.sort_values(by='due_date_dt', ascending=True)
    
    # Renderizar as 3 colunas principais do Kanban
    col_internas, col_externas, col_eventos = st.columns(3)
    
    with col_internas:
        st.subheader(CATEGORIES["interna"])
        if user['profile'] == 'Recepção':
            st.info("Acesso restrito para o seu perfil.")
        else:
            if not df.empty:
                df_interna = df[df['category'] == 'interna']
                st.write(f"*{len(df_interna)} agendamentos*")
                for _, row in df_interna.iterrows():
                    render_card(row, user['profile'], user['email'])
            else:
                st.write("*Vazio*")
                
    with col_externas:
        st.subheader(CATEGORIES["externa"])
        if not df.empty:
            df_externa = df[df['category'] == 'externa']
            st.write(f"*{len(df_externa)} agendamentos*")
            for _, row in df_externa.iterrows():
                render_card(row, user['profile'], user['email'])
        else:
            st.write("*Vazio*")
            
    with col_eventos:
        st.subheader(CATEGORIES["evento"])
        if not df.empty:
            df_evento = df[df['category'] == 'evento']
            st.write(f"*{len(df_evento)} agendamentos*")
            for _, row in df_evento.iterrows():
                render_card(row, user['profile'], user['email'])
        else:
            st.write("*Vazio*")

@st.fragment(run_every=10)
def render_done_board(user):
    st.header("✅ Cartões Concluídos")
    st.write("Abaixo estão os cartões finalizados e arquivados do painel principal.")
    df_all = get_visible_cards(user['profile'], user['email'])
    df_concluidos = df_all[df_all['status'] == 'concluido'] if not df_all.empty and 'status' in df_all.columns else pd.DataFrame()
    
    if not df_concluidos.empty:
        df_concluidos['due_date_dt'] = pd.to_datetime(df_concluidos['due_date'])
        df_concluidos = df_concluidos.sort_values(by='due_date_dt', ascending=False)
        
        # Mostra numa grade de 4 colunas (responsivo)
        cols = st.columns(4)
        for idx, row in df_concluidos.reset_index().iterrows():
            with cols[idx % 4]:
                render_card(row, user['profile'], user['email'], read_only=True)
    else:
        st.info("Nenhum cartão concluído no momento.")
def main():
    if not check_auth():
        return
        
    user = st.session_state['user']
    
    # Header
    col_logo, col_user = st.columns([8, 2])
    with col_logo:
        st.title(f"📅 Port.Ico - Acessando como {user['profile']}")
    with col_user:
        st.write(f"Olá, **{user['name']}**")
        b1, b2 = st.columns(2)
        with b1:
            if st.button("Sobre"):
                about_modal()
        with b2:
            if st.button("Sair"):
                logout()
            
    st.divider()
    
    if user['profile'] == 'Presidência':
        tab_kanban, tab_done, tab_utils = st.tabs(["📊 Port.Ico", "✅ Concluídos", "⚙️ Utilitários"])
    else:
        tab_kanban, tab_done = st.tabs(["📊 Port.Ico", "✅ Concluídos"])
        tab_utils = None


    with tab_kanban:
        render_kanban_board(user)

    with tab_done:
        render_done_board(user)

    if tab_utils:
        with tab_utils:
            st.header("⚙️ Configurações e Utilitários")
            
            with st.expander("Manutenção de Diretores"):
                st.write("Gerencie as opções que aparecem na lista de Diretores.")
                d_col1, d_col2, d_col3 = st.columns(3)
                with d_col1:
                    new_dir = st.text_input("Novo Diretor")
                    new_dir_color = st.selectbox("Cor", COLORS, key="ndc")
                    if st.button("Adicionar Diretor", use_container_width=True):
                        add_director(new_dir, new_dir_color)
                        st.rerun()
                with d_col2:
                    dirs_dict = get_directors_dict()
                    dirs = list(dirs_dict.keys())
                    target_dir = st.selectbox("Selecione para Alterar/Remover", [""] + dirs, key="target_dir")
                    if st.button("Remover Diretor", use_container_width=True):
                        remove_director(target_dir)
                        st.rerun()
                with d_col3:
                    st.write("") # Espaçamento
                    st.write("")
                    if st.button("Editar Diretor", use_container_width=True, disabled=not target_dir):
                        edit_director_modal(target_dir, dirs_dict.get(target_dir, "green"))
                st.write("**Lista atual:**")
                st.dataframe(pd.DataFrame(list(dirs_dict.items()), columns=["Diretor", "Cor"]), use_container_width=True, hide_index=True)
                        
            with st.expander("Manutenção de Salas"):
                st.write("Gerencie as opções que aparecem na lista de Salas.")
                r_col1, r_col2, r_col3 = st.columns(3)
                with r_col1:
                    new_room = st.text_input("Nova Sala")
                    new_room_color = st.selectbox("Cor", COLORS, key="nrc", index=COLORS.index("purple"))
                    if st.button("Adicionar Sala", use_container_width=True):
                        add_room(new_room, new_room_color)
                        st.rerun()
                with r_col2:
                    rooms_dict = get_rooms_dict()
                    rooms = list(rooms_dict.keys())
                    target_room = st.selectbox("Selecione para Alterar/Remover", [""] + rooms, key="target_room")
                    if st.button("Remover Sala", use_container_width=True):
                        remove_room(target_room)
                        st.rerun()
                with r_col3:
                    st.write("") # Espaçamento
                    st.write("")
                    if st.button("Editar Sala", use_container_width=True, disabled=not target_room):
                        edit_room_modal(target_room, rooms_dict.get(target_room, "purple"))
                st.write("**Lista atual:**")
                st.dataframe(pd.DataFrame(list(rooms_dict.items()), columns=["Sala", "Cor"]), use_container_width=True, hide_index=True)
                        
            with st.expander("Manutenção de Serviços Adicionais"):
                st.write("Gerencie as opções que aparecem na lista de Serviços.")
                s_col1, s_col2, s_col3 = st.columns(3)
                with s_col1:
                    new_svc = st.text_input("Novo Serviço")
                    new_svc_color = st.selectbox("Cor", COLORS, key="nsc", index=COLORS.index("brown"))
                    if st.button("Adicionar Serviço", use_container_width=True):
                        add_service(new_svc, new_svc_color)
                        st.rerun()
                with s_col2:
                    svcs_dict = get_services_dict()
                    svcs = list(svcs_dict.keys())
                    target_svc = st.selectbox("Selecione para Alterar/Remover", [""] + svcs, key="target_svc")
                    if st.button("Remover Serviço", use_container_width=True):
                        remove_service(target_svc)
                        st.rerun()
                with s_col3:
                    st.write("") # Espaçamento
                    st.write("")
                    if st.button("Editar Serviço", use_container_width=True, disabled=not target_svc):
                        edit_service_modal(target_svc, svcs_dict.get(target_svc, "brown"))
                st.write("**Lista atual:**")
                st.dataframe(pd.DataFrame(list(svcs_dict.items()), columns=["Serviço", "Cor"]), use_container_width=True, hide_index=True)
                        
            with st.expander("Gerenciar Perfis de Acesso"):
                st.write("Gerencie quem pode acessar o sistema.")
                users_df = get_users()
                st.dataframe(users_df.drop(columns=['password'], errors='ignore'), use_container_width=True)
                
                u_col1, u_col2 = st.columns(2)
                with u_col1:
                    st.subheader("Novo Usuário")
                    with st.form("new_user_form"):
                        n_email = st.text_input("E-mail")
                        n_name = st.text_input("Nome")
                        n_pass = st.text_input("Senha", type="password")
                        n_profile = st.selectbox("Perfil", ["Presidência", "Pool", "Recepção", "TI", "Copa"])
                        if st.form_submit_button("Criar Usuário"):
                            if n_email and n_pass:
                                add_user(n_email, n_pass, n_profile, n_name)
                                st.rerun()
                with u_col2:
                    st.subheader("Remover Usuário")
                    with st.form("del_user_form"):
                        del_email = st.selectbox("Selecione o E-mail", [""] + users_df['email'].tolist())
                        if st.form_submit_button("Excluir Usuário"):
                            if del_email and del_email != user['email']:
                                remove_user(del_email)
                                st.rerun()

if __name__ == "__main__":
    main()
