import pandas as pd
import os
import uuid
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.csv")
CARDS_FILE = os.path.join(DATA_DIR, "cards.csv")
LOGS_FILE = os.path.join(DATA_DIR, "logs.csv")

def get_users():
    if os.path.exists(USERS_FILE):
        return pd.read_csv(USERS_FILE)
    return pd.DataFrame()

def get_cards():
    if os.path.exists(CARDS_FILE):
        dtypes = {
            'people_count': str,
            'director_name': str,
            'room_location': str,
            'catering_services': str,
            'description': str,
            'title': str
        }
        df = pd.read_csv(CARDS_FILE, dtype=dtypes)
        # Convert string to bool where appropriate
        if 'requires_ti' in df.columns:
            df['requires_ti'] = df['requires_ti'].astype(bool)
        if 'has_car_access' in df.columns:
            df['has_car_access'] = df['has_car_access'].astype(bool)
        
        # Replace 'nan' strings with empty strings resulting from empty CSV cells
        for col in dtypes.keys():
            if col in df.columns:
                df.loc[df[col].isna(), col] = ""
                
        if 'status' not in df.columns:
            df['status'] = 'active'
        
        return df
    return pd.DataFrame(columns=['id', 'title', 'category', 'secretary_group', 'director_name', 
                                 'room_location', 'people_count', 'requires_ti', 'has_car_access', 
                                 'catering_services', 'due_date', 'description', 'status', 'created_by', 'created_at'])

def save_cards(df):
    df.to_csv(CARDS_FILE, index=False)

def get_logs(card_id):
    if os.path.exists(LOGS_FILE):
        df = pd.read_csv(LOGS_FILE)
        df_logs = df[df['card_id'] == card_id]
        if not df_logs.empty:
            df_logs['timestamp_dt'] = pd.to_datetime(df_logs['timestamp'])
            df_logs = df_logs.sort_values(by='timestamp_dt', ascending=False)
            return df_logs.to_dict('records')
    return []

def add_log(card_id, user_email, action, details):
    log_entry = {
        'id': str(uuid.uuid4()),
        'card_id': card_id,
        'timestamp': datetime.now().isoformat(),
        'user_email': user_email,
        'action': action,
        'details': details
    }
    
    if os.path.exists(LOGS_FILE):
        df = pd.read_csv(LOGS_FILE)
    else:
        df = pd.DataFrame(columns=['id', 'card_id', 'timestamp', 'user_email', 'action', 'details'])
        
    df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
    df.to_csv(LOGS_FILE, index=False)

def create_card(card_data):
    df = get_cards()
    card_data['id'] = str(uuid.uuid4())
    card_data['created_at'] = datetime.now().isoformat()
    card_data['status'] = 'active'
    # ensure correct types
    card_data['requires_ti'] = bool(card_data.get('requires_ti', False))
    card_data['has_car_access'] = bool(card_data.get('has_car_access', False))
    for list_col in ['catering_services', 'director_name', 'room_location']:
        if isinstance(card_data.get(list_col), list):
            card_data[list_col] = ",".join(card_data[list_col])
        
    new_card_df = pd.DataFrame([card_data])
    df = pd.concat([df, new_card_df], ignore_index=True)
    save_cards(df)
    
    # Gerar log de criação
    user_email = card_data.get('created_by', 'sistema')
    add_log(card_data['id'], user_email, "Criação", f"Criou o agendamento '{card_data.get('title', '')}'.")
    return card_data['id']

def update_card(card_id, update_data, user_email="sistema", action_name="Atualização"):
    df = get_cards()
    if df.empty or card_id not in df['id'].values:
        return False
        
    idx = df.index[df['id'] == card_id].tolist()[0]
    
    changes = []
    
    for key, value in update_data.items():
        if key in df.columns:
            if key in ['catering_services', 'director_name', 'room_location'] and isinstance(value, list):
                value = ",".join(value)
            
            old_val = str(df.at[idx, key])
            new_val = str(value)
            
            if old_val != new_val:
                # Dicionário de tradução para os logs ficarem bonitos
                field_names = {
                    'title': 'Título', 'category': 'Categoria', 'due_date': 'Data/Hora',
                    'director_name': 'Diretor', 'room_location': 'Local/Sala',
                    'people_count': 'Qtd. Pessoas', 'description': 'Observações',
                    'requires_ti': 'Suporte TI', 'has_car_access': 'Vaga Carro',
                    'catering_services': 'Serviços', 'status': 'Status'
                }
                friendly_key = field_names.get(key, key)
                changes.append(f"Alterou {friendly_key} de '{old_val}' para '{new_val}'")
                
            df.at[idx, key] = value
            
    save_cards(df)
    
    if changes:
        add_log(card_id, user_email, action_name, " | ".join(changes))
    elif action_name != "Atualização":
        add_log(card_id, user_email, action_name, action_name)
        
    return True

def delete_card(card_id):
    df = get_cards()
    if not df.empty and card_id in df['id'].values:
        df = df[df['id'] != card_id]
        save_cards(df)
        return True
    return False

def get_visible_cards(user_profile, user_email):
    df = get_cards()
    if df.empty:
        return df
        
    # RLS Application level filtering
    if user_profile == 'Presidência':
        # Vê tudo
        return df
    elif user_profile == 'Pool':
        # Vê apenas os criados pelo Pool
        return df[df['secretary_group'] == 'pool']
    elif user_profile == 'TI':
        # Vê apenas cards com requires_ti == True
        return df[df['requires_ti'] == True]
    elif user_profile == 'Recepção':
        # Não vê Internas
        return df[df['category'] != 'interna']
    elif user_profile == 'Copa':
        # Vê tudo (para apoiar na logística)
        return df
    else:
        # Padrão restrito
        return df[df['created_by'] == user_email]

DIRECTORS_FILE = os.path.join(DATA_DIR, "directors.csv")
ROOMS_FILE = os.path.join(DATA_DIR, "rooms.csv")

def get_directors():
    if os.path.exists(DIRECTORS_FILE):
        return sorted(pd.read_csv(DIRECTORS_FILE)['name'].dropna().astype(str).tolist())
    return []

def get_directors_dict():
    if os.path.exists(DIRECTORS_FILE):
        df = pd.read_csv(DIRECTORS_FILE)
        df = df.sort_values(by='name')
        if 'color' in df.columns:
            return dict(zip(df['name'], df['color']))
        else:
            return {n: 'green' for n in df['name']}
    return {}

def add_director(name, color='green'):
    if name and name not in get_directors():
        df = pd.DataFrame([{'name': name, 'color': color}])
        if os.path.exists(DIRECTORS_FILE):
            old_df = pd.read_csv(DIRECTORS_FILE)
            df = pd.concat([old_df, df], ignore_index=True)
        df.to_csv(DIRECTORS_FILE, index=False)

def remove_director(name):
    if os.path.exists(DIRECTORS_FILE):
        df = pd.read_csv(DIRECTORS_FILE)
        df = df[df['name'] != name]
        df.to_csv(DIRECTORS_FILE, index=False)

def update_director(old_name, new_name, color='green'):
    if os.path.exists(DIRECTORS_FILE) and new_name:
        df = pd.read_csv(DIRECTORS_FILE)
        if 'color' not in df.columns:
            df['color'] = 'green'
        df.loc[df['name'] == old_name, ['name', 'color']] = [new_name, color]
        df.to_csv(DIRECTORS_FILE, index=False)

def get_rooms():
    if os.path.exists(ROOMS_FILE):
        return sorted(pd.read_csv(ROOMS_FILE)['name'].dropna().astype(str).tolist())
    return []

def get_rooms_dict():
    if os.path.exists(ROOMS_FILE):
        df = pd.read_csv(ROOMS_FILE)
        df = df.sort_values(by='name')
        if 'color' in df.columns:
            return dict(zip(df['name'], df['color']))
        else:
            return {n: 'purple' for n in df['name']}
    return {}

def add_room(name, color='purple'):
    if name and name not in get_rooms():
        df = pd.DataFrame([{'name': name, 'color': color}])
        if os.path.exists(ROOMS_FILE):
            old_df = pd.read_csv(ROOMS_FILE)
            df = pd.concat([old_df, df], ignore_index=True)
        df.to_csv(ROOMS_FILE, index=False)

def remove_room(name):
    if os.path.exists(ROOMS_FILE):
        df = pd.read_csv(ROOMS_FILE)
        df = df[df['name'] != name]
        df.to_csv(ROOMS_FILE, index=False)

def update_room(old_name, new_name, color='purple'):
    if os.path.exists(ROOMS_FILE) and new_name:
        df = pd.read_csv(ROOMS_FILE)
        if 'color' not in df.columns:
            df['color'] = 'purple'
        df.loc[df['name'] == old_name, ['name', 'color']] = [new_name, color]
        df.to_csv(ROOMS_FILE, index=False)

SERVICES_FILE = os.path.join(DATA_DIR, "services.csv")

def get_services():
    if os.path.exists(SERVICES_FILE):
        return sorted(pd.read_csv(SERVICES_FILE)['name'].dropna().astype(str).tolist())
    return []

def get_services_dict():
    if os.path.exists(SERVICES_FILE):
        df = pd.read_csv(SERVICES_FILE)
        df = df.sort_values(by='name')
        if 'color' in df.columns:
            return dict(zip(df['name'], df['color']))
        else:
            return {n: 'brown' for n in df['name']}
    return {}

def add_service(name, color='brown'):
    if name and name not in get_services():
        df = pd.DataFrame([{'name': name, 'color': color}])
        if os.path.exists(SERVICES_FILE):
            old_df = pd.read_csv(SERVICES_FILE)
            df = pd.concat([old_df, df], ignore_index=True)
        df.to_csv(SERVICES_FILE, index=False)

def remove_service(name):
    if os.path.exists(SERVICES_FILE):
        df = pd.read_csv(SERVICES_FILE)
        df = df[df['name'] != name]
        df.to_csv(SERVICES_FILE, index=False)

def update_service(old_name, new_name, color='brown'):
    if os.path.exists(SERVICES_FILE) and new_name:
        df = pd.read_csv(SERVICES_FILE)
        if 'color' not in df.columns:
            df['color'] = 'brown'
        df.loc[df['name'] == old_name, ['name', 'color']] = [new_name, color]
        df.to_csv(SERVICES_FILE, index=False)

def add_user(email, password, profile, name):
    users_df = get_users()
    if email not in users_df['email'].values:
        df = pd.DataFrame([{'email': email, 'password': password, 'profile': profile, 'name': name}])
        df = pd.concat([users_df, df], ignore_index=True)
        df.to_csv(USERS_FILE, index=False)

def remove_user(email):
    users_df = get_users()
    if email in users_df['email'].values:
        df = users_df[users_df['email'] != email]
        df.to_csv(USERS_FILE, index=False)


