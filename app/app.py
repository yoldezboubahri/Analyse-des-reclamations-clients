# -*- coding: utf-8 -*-
"""
app.py
------
Point d'entrée de l'application Streamlit "Attijari bank — Analyse Client".
Ce fichier ne fait que de l'orchestration : configuration de la page,
chargement des modèles, initialisation du session_state, navigation entre
les pages Accueil / Détails, et pied de page.

Toute la logique métier est répartie dans les modules du dossier :
config.py, utils.py, models.py, icons.py, styles.py, pagination.py,
exports.py, stats_view.py, view_accueil.py, view_details.py.
"""

import streamlit as st

from styles import configurer_page, injecter_css, afficher_header, afficher_footer
from models import load_pipeline
import view_accueil
import view_details

# ------------------------------------------------------------------
# Configuration de la page + CSS 
# ------------------------------------------------------------------
configurer_page()
injecter_css()

# ------------------------------------------------------------------
# En-tête
# ------------------------------------------------------------------
afficher_header()

sent_tok, sent_model, churn_tok, churn_model = load_pipeline()

# ------------------------------------------------------------------
# Session state
# ------------------------------------------------------------------
if "historique" not in st.session_state:
    st.session_state.historique = []

if "input_key" not in st.session_state:
    st.session_state.input_key = 0

if "tous_resultats" not in st.session_state:
    st.session_state.tous_resultats = []

if "df_stats" not in st.session_state:
    st.session_state.df_stats = None

if "page" not in st.session_state:
    st.session_state.page = "accueil"

# ------------------------------------------------------------------
# Navigation
# ------------------------------------------------------------------
nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 2])
with nav_col1:
    if st.button(" Accueil", type="primary" if st.session_state.page == "accueil" else "secondary"):
        st.session_state.page = "accueil"
        st.rerun()
with nav_col2:
    details_dispo = st.session_state.df_stats is not None and not st.session_state.df_stats.empty
    if st.button(" Détails", type="primary" if st.session_state.page == "details" else "secondary", disabled=not details_dispo):
        st.session_state.page = "details"
        st.rerun()

if st.session_state.page == "accueil":
    view_accueil.render(sent_tok, sent_model, churn_tok, churn_model)
elif st.session_state.page == "details":
    view_details.render()

# ------------------------------------------------------------------
# Pied de page
# ------------------------------------------------------------------
afficher_footer()
