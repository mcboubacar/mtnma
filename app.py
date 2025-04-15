
import streamlit as st
import os
from hashlib import sha256

st.set_page_config(page_title="Suivi des Activités TIC", layout="wide")

# --- Simulation d'authentification utilisateur ---
# USERS = {
#     "alice": sha256("motdepasse1".encode()).hexdigest(),
#     "bob": sha256("motdepasse2".encode()).hexdigest(),
#     "admin": sha256("adminpass".encode()).hexdigest()
# }

# # --- Fonction d'authentification ---
# def login():
#     st.sidebar.title("Authentification")
#     username = st.sidebar.text_input("Nom d'utilisateur")
#     password = st.sidebar.text_input("Mot de passe", type="password")
#     if st.sidebar.button("Se connecter"):
#         hashed = sha256(password.encode()).hexdigest()
#         if username in USERS and USERS[username] == hashed:
#             st.session_state["user"] = username
#             st.success(f"Bienvenue, {username} !")
#         else:
#             st.error("Identifiants invalides")

# --- Configuration du mode de source de données ---
# st.sidebar.markdown("---")
# mode = st.sidebar.radio("Source des données", ["Excel", "SharePoint"])
# os.environ["USE_SHAREPOINT"] = "true" if mode == "SharePoint" else "false"

# --- Lancement de l'application ---
st.title("Suivi des Activités TIC")

# # --- Authentification ---
# if "user" not in st.session_state:
#     login()
#     st.stop()

# st.success(f"Connecté en tant que {st.session_state['user']}")
