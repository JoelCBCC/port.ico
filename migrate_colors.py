import pandas as pd
import os

DATA_DIR = "data"
DIRECTORS_FILE = os.path.join(DATA_DIR, "directors.csv")
ROOMS_FILE = os.path.join(DATA_DIR, "rooms.csv")
SERVICES_FILE = os.path.join(DATA_DIR, "services.csv")

# 1. Directors -> all green
if os.path.exists(DIRECTORS_FILE):
    df = pd.read_csv(DIRECTORS_FILE)
    if 'color' not in df.columns:
        df['color'] = 'green'
        df.to_csv(DIRECTORS_FILE, index=False)
        print("Updated directors.csv")

# 2. Rooms -> lilac or purple
lilac_rooms = ['CAD', 'DIR 1', 'DIR 2', 'DIR 3', 'DIR 4', 'DIR 5', 'PRE', 'SL DANIEL', 'SL DIOGO', 'SL FELIPE', 'SL VICENTE', 'SL YURI', 'COPA']
if os.path.exists(ROOMS_FILE):
    df = pd.read_csv(ROOMS_FILE)
    if 'color' not in df.columns:
        df['color'] = df['name'].apply(lambda x: 'lilac' if str(x).strip() in lilac_rooms else 'purple')
        df.to_csv(ROOMS_FILE, index=False)
        print("Updated rooms.csv")

# 3. Services -> red or brown
red_services = ["ESTRELA", "IFOOD", "ENTREGA"]
if os.path.exists(SERVICES_FILE):
    df = pd.read_csv(SERVICES_FILE)
    if 'color' not in df.columns:
        df['color'] = df['name'].apply(lambda x: 'red' if str(x).strip() in red_services else 'brown')
        df.to_csv(SERVICES_FILE, index=False)
        print("Updated services.csv")
