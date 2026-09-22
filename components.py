import streamlit as st
import datetime
import pandas as pd
from models import CATEGORIES
from database import create_card, update_card, get_directors, get_rooms, get_services, get_directors_dict, get_rooms_dict, get_services_dict, delete_card, get_logs

@st.dialog("Novo Agendamento")
def create_card_modal(user_email, user_profile, initial_category="interna"):
    st.write(f"Criando novo cartão como: **{st.session_state['user']['name']}**")
    
    title = st.text_input("Título (ex: 15h00 - Giselle + Beto)")
    
    options_keys = list(CATEGORIES.keys())
    if user_profile == "Recepção":
        options_keys = ["externa", "evento"]
        
    category = st.selectbox("Categoria (Coluna)", options=options_keys, format_func=lambda x: CATEGORIES[x], index=options_keys.index(initial_category) if initial_category in options_keys else 0)
    
    col1, col2 = st.columns(2)
    with col1:
        director = st.multiselect("Diretores", get_directors())
        people = st.text_input("Qtd Pessoas (ex: 8p)")
        date = st.date_input("Data do Evento", datetime.date.today())
    with col2:
        room = st.multiselect("Salas", get_rooms())
        time_val = st.time_input("Hora do Evento", datetime.time(9, 0))
        
    st.write("Serviços Adicionais")
    req_ti = st.checkbox("Requer apoio de TI (Service Desk)")
    req_car = st.checkbox("Acesso autorizado com veículo (CARRO)")
    
    catering = st.multiselect("Serviços Adicionais", get_services())
    
    description = st.text_area("Observações")
    
    if st.button("Salvar", type="primary"):
        if not title:
            st.error("O título é obrigatório.")
        else:
            sec_group = "presidencia" if user_profile == "Presidência" else "pool"
            
            due_datetime = datetime.datetime.combine(date, time_val).isoformat()
            card_data = {
                "title": title,
                "category": category,
                "secretary_group": sec_group,
                "director_name": director,
                "room_location": room,
                "people_count": people,
                "requires_ti": req_ti,
                "has_car_access": req_car,
                "catering_services": catering,
                "due_date": due_datetime,
                "description": description,
                "created_by": user_email
            }
            create_card(card_data)
            st.success("Cartão criado!")
            st.rerun()

@st.dialog("Mover Agendamento")
def move_card_modal(card_id, current_category, user_email):
    new_cat = st.radio("Mover para:", list(CATEGORIES.keys()), format_func=lambda x: CATEGORIES[x], index=list(CATEGORIES.keys()).index(current_category))
    if st.button("Confirmar Movimentação", type="primary", key=f"move_btn_{card_id}"):
        update_card(card_id, {"category": new_cat}, user_email, "Movimentação")
        st.success("Movido com sucesso!")
        st.rerun()

@st.dialog("Editar Agendamento")
def edit_card_modal(row, user_email):
    st.write(f"Editando: **{row['title']}**")
    
    title = st.text_input("Título", value=row['title'], key=f"edit_title_{row['id']}")
    
    col1, col2 = st.columns(2)
    with col1:
        cur_dirs = str(row['director_name']).split(",") if pd.notna(row['director_name']) and row['director_name'] else []
        cur_dirs = [d.strip() for d in cur_dirs if d.strip() in get_directors()]
        director = st.multiselect("Diretores", get_directors(), default=cur_dirs, key=f"edit_dir_{row['id']}")
        
        people = st.text_input("Qtd Pessoas", value=row.get('people_count', ''), key=f"edit_ppl_{row['id']}")
        
        dt = datetime.datetime.fromisoformat(row['due_date'])
        date = st.date_input("Data do Evento", dt.date(), key=f"edit_date_{row['id']}")
    with col2:
        cur_rooms = str(row['room_location']).split(",") if pd.notna(row['room_location']) and row['room_location'] else []
        cur_rooms = [r.strip() for r in cur_rooms if r.strip() in get_rooms()]
        room = st.multiselect("Salas", get_rooms(), default=cur_rooms, key=f"edit_room_{row['id']}")
        
        time_val = st.time_input("Hora do Evento", dt.time(), key=f"edit_time_{row['id']}")
        
    st.write("Serviços Adicionais")
    req_ti = st.checkbox("Requer apoio de TI", value=bool(row.get('requires_ti', False)), key=f"edit_ti_{row['id']}")
    req_car = st.checkbox("Acesso com veículo", value=bool(row.get('has_car_access', False)), key=f"edit_car_{row['id']}")
    
    cur_cat = str(row['catering_services']).split(",") if pd.notna(row['catering_services']) and row['catering_services'] else []
    cur_cat = [c.strip() for c in cur_cat if c.strip() in get_services()]
    catering = st.multiselect("Serviços Adicionais", get_services(), default=cur_cat, key=f"edit_cat_{row['id']}")
    
    description = st.text_area("Observações", value=row.get('description', ''), key=f"edit_desc_{row['id']}")
    
    if st.button("Salvar Alterações", type="primary", key=f"edit_save_{row['id']}"):
        if not title:
            st.error("O título é obrigatório.")
        else:
            due_datetime = datetime.datetime.combine(date, time_val).isoformat()
            update_data = {
                "title": title,
                "director_name": director,
                "room_location": room,
                "people_count": people,
                "requires_ti": req_ti,
                "has_car_access": req_car,
                "catering_services": catering,
                "due_date": due_datetime,
                "description": description
            }
            update_card(row['id'], update_data, user_email, "Edição")
            st.success("Cartão atualizado!")
            st.rerun()

def render_card(row, current_user_profile, user_email, read_only=False):
    dir_dict = get_directors_dict()
    room_dict = get_rooms_dict()
    svc_dict = get_services_dict()

    with st.container(border=True):
        title_style = "margin:0; padding:0; color:#333;"
        if current_user_profile in ["TI", "Copa"]:
            title_style += " filter: blur(5px); user-select: none;"
            
        st.markdown(f"""
        <div style='margin: -16px -16px 16px -16px; padding: 12px 16px; background-color: #ffecd9; border: 1px solid rgba(49, 51, 63, 0.2); border-radius: 8px 8px 0 0; box-sizing: border-box;'>
            <h4 style='{title_style}'>📌 {row['title']}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<div style='font-size: 0.85em; color: #555; margin-bottom: 5px;'>{datetime.datetime.fromisoformat(row['due_date']).strftime('%d/%m/%Y %H:%M')}</div>", unsafe_allow_html=True)
        
        if pd.notna(row.get('description')) and str(row['description']).strip():
            st.markdown(f"<div style='font-size: 0.85em; color: #444; margin-bottom: 10px; font-style: italic;'>{row['description']}</div>", unsafe_allow_html=True)
        
        def badge(text, color):
            bg = {
                "green": "#e3fce0", 
                "light_green": "#f0fdf0", 
                "brown": "#f4e6d9", 
                "red": "#fce0e0",
                "lilac": "#f3e8ff",
                "purple": "#e9d5ff",
                "blue": "#e0f0fc",
                "yellow": "#fcf5e0",
                "gray": "#e0e0e0"
            }.get(color, "#e0e0e0")
            
            c = {
                "green": "#1e6b12", 
                "light_green": "#2c8a24", 
                "brown": "#6e4c2b", 
                "red": "#8a1616",
                "lilac": "#7e22ce",
                "purple": "#581c87",
                "blue": "#0c4980",
                "yellow": "#785f0a",
                "gray": "#333"
            }.get(color, "#333")
            return f'<span style="background-color: {bg}; color: {c}; padding: 2px 6px; border-radius: 4px; font-size: 11px; margin-right: 4px; display: inline-block; margin-bottom: 4px;">{text}</span>'

        badges = []
        if pd.notna(row['director_name']) and row['director_name']:
            dirs = str(row['director_name']).split(",")
            for d in dirs:
                if d.strip(): 
                    badges.append(badge(d.strip(), dir_dict.get(d.strip(), "gray")))
            
        if pd.notna(row['room_location']) and row['room_location']:
            rooms = str(row['room_location']).split(",")
            for r in rooms:
                if r.strip():
                    badges.append(badge(r.strip(), room_dict.get(r.strip(), "gray")))
            
        if row.get('requires_ti'):
            badges.append(badge("TI", "red"))
        if row.get('has_car_access'):
            badges.append(badge("CARRO", "red"))
            
        if pd.notna(row.get('people_count')) and row['people_count']:
            badges.append(badge(row['people_count'], "blue"))
            
        if pd.notna(row.get('catering_services')) and row['catering_services']:
            services = str(row['catering_services']).split(",")
            for svc in services:
                if svc.strip():
                    badges.append(badge(svc.strip(), svc_dict.get(svc.strip(), "gray")))
                
        if badges:
            st.markdown("<div style='margin-bottom: 10px;'>" + "".join(badges) + "</div>", unsafe_allow_html=True)
            
        if current_user_profile in ["Presidência", "Pool"]:
            st.markdown("<hr style='margin: 10px 0; border: 0; border-top: 1px solid #eeeeee;'>", unsafe_allow_html=True)
            # Suaviza as bordas dos botões apenas dentro dos cartões
            st.markdown("""
                <style>
                div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stButton"] button[kind="secondary"] {
                    border-color: rgba(0,0,0,0.1) !important;
                    background-color: transparent !important;
                    box-shadow: none !important;
                }
                div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stButton"] button[kind="secondary"]:hover {
                    border-color: rgba(0,0,0,0.3) !important;
                    background-color: #f7f7f7 !important;
                }
                div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stButton"] p {
                    font-size: 0.85em !important;
                }
                /* Alinha os botões à direita sempre */
                div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stButton"] {
                    display: flex;
                    justify-content: flex-end;
                    width: 100%;
                }
                /* Tenta forçar os botões a ficarem na horizontal no celular */
                @media (max-width: 640px) {
                    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stHorizontalBlock"] {
                        flex-direction: row !important;
                        flex-wrap: wrap !important;
                        justify-content: flex-end !important;
                    }
                    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
                        width: auto !important;
                        min-width: 0 !important;
                        flex: 0 0 auto !important;
                    }
                }
                </style>
            """, unsafe_allow_html=True)
            
            if not read_only:
                col_space, b_obs, b_log, b1, b2, b3 = st.columns([1.6, 1.2, 1.2, 1.2, 1.2, 1.2])
                with b_obs:
                    if st.button("👁️", key=f"obs_btn_{row['id']}", help="Ver Observações"):
                        show_observations_modal(row['title'], row.get('description', ''))
                with b_log:
                    if st.button("💬", key=f"log_btn_{row['id']}", help="Ver Histórico"):
                        show_logs_modal(row['id'], row['title'])
                with b1:
                    if st.button("✅", key=f"done_btn_{row['id']}", help="Concluir Cartão"):
                        update_card(row['id'], {'status': 'concluido'}, user_email, "Conclusão")
                        st.rerun()
                with b2:
                    if st.button("✏️", key=f"edit_btn_{row['id']}", help="Editar Cartão"):
                        edit_card_modal(row, user_email)
                with b3:
                    if st.button("➡️", key=f"move_btn2_{row['id']}", help="Mover Cartão"):
                        move_card_modal(row['id'], row['category'], user_email)
            else:
                col_space, b_obs, b_log, b1 = st.columns([4.0, 1.2, 1.2, 1.2])
                with b_obs:
                    if st.button("👁️", key=f"obs_btn_{row['id']}", help="Ver Observações"):
                        show_observations_modal(row['title'], row.get('description', ''))
                with b_log:
                    if st.button("💬", key=f"log_btn_{row['id']}", help="Ver Histórico"):
                        show_logs_modal(row['id'], row['title'])
                with b1:
                    if st.button("⏪", key=f"reopen_btn_{row['id']}", help="Reabrir Cartão (Voltar para o Port.Ico)"):
                        update_card(row['id'], {'status': 'active'}, user_email, "Reabertura")
                        st.rerun()

@st.dialog("Observações")
def show_observations_modal(title, description):
    st.write(f"Observações de: **{title}**")
    if pd.notna(description) and str(description).strip():
        st.info(description)
    else:
        st.warning("Nenhuma observação registrada para este agendamento.")

@st.dialog("Histórico do Agendamento")
def show_logs_modal(card_id, title):
    st.write(f"Histórico de: **{title}**")
    logs = get_logs(card_id)
    
    if not logs:
        st.info("Nenhum histórico encontrado para este cartão.")
        return
        
    for log in logs:
        dt = datetime.datetime.fromisoformat(log['timestamp']).strftime('%d/%m/%Y %H:%M:%S')
        st.markdown(f"""
        <div style="margin-bottom: 15px; padding: 10px; border-left: 3px solid #ffccaa; background-color: #fcfcfc;">
            <div style="font-size: 0.85em; color: #777; margin-bottom: 5px;">
                <strong>{log['action']}</strong> por {log['user_email']} em {dt}
            </div>
            <div style="font-size: 0.95em; color: #333;">
                {log['details']}
            </div>
        </div>
        """, unsafe_allow_html=True)
