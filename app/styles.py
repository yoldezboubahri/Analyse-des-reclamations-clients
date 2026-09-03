# -*- coding: utf-8 -*-
"""
styles.py
---------
Configuration de la page Streamlit et injection du CSS "Attijari bank".
"""

import streamlit as st

from config import (
    ROUGE_FONCE, ROUGE, ORANGE, ORANGE_CLAIR, JAUNE, NOIR,
    GRIS_TEXTE, BLANC, VERT, VERT_CLAIR, BORDURE,
)


def configurer_page():
    """A appeler en tout premier, avant tout autre appel st.*"""
    st.set_page_config(page_title="Attijari bank — Analyse Client", page_icon="🏦", layout="centered")


def injecter_css():
    st.markdown(
        f"""
        <style>
            .stApp {{ background-color: #EAEAE7; }}
            .block-container {{ padding-top: 1.4rem; max-width: 820px; }}

            /* En-tête */
            .aw-header {{
                background: linear-gradient(135deg, {ROUGE_FONCE} 0%, {ROUGE} 100%);
                padding: 30px 34px;
                border-radius: 20px;
                margin-bottom: 28px;
                box-shadow: 0 8px 24px rgba(122,27,30,0.28);
                display: flex;
                align-items: center;
                gap: 22px;
            }}
            .aw-logo {{
                background: {BLANC};
                border-radius: 16px;
                width: 130px; height: 130px;
                display: flex; align-items: center; justify-content: center;
                flex-shrink: 0;
                padding: 12px;
                box-shadow: 0 4px 14px rgba(0,0,0,0.18);
            }}
            .aw-header-text h1 {{
                color: {BLANC}; font-size: 27px; font-weight: 800; margin: 0; letter-spacing: 0.2px;
            }}
            .aw-header-text p {{
                color: {BLANC}; opacity: 0.92; font-size: 14px; margin: 5px 0 0 0;
            }}

            /* Cartes de section */
            .aw-card {{
                background: {BLANC};
                border-radius: 18px;
                padding: 26px 28px;
                box-shadow: 0 4px 16px rgba(0,0,0,0.08);
                border: 1px solid #DCDCD8;
                margin-bottom: 22px;
            }}
            .aw-card-title {{
                font-size: 14px;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.7px;
                color: {NOIR};
                margin-bottom: 16px;
                display: flex; align-items: center; gap: 9px;
            }}

            .stTextArea textarea {{
                border: 1.5px solid {BORDURE} !important;
                border-radius: 12px !important;
                font-size: 15px !important;
                background-color: #FAFAF9 !important;
            }}
            .stTextArea textarea:focus {{ border-color: {ORANGE} !important; box-shadow: 0 0 0 1px {ORANGE} !important; }}
            .stTextArea label {{ display: none; }}

            div.stButton > button {{
                background: linear-gradient(135deg, {ORANGE_CLAIR} 0%, {ORANGE} 100%);
                color: {BLANC}; font-weight: 700; font-size: 15px;
                padding: 12px 26px; border-radius: 12px; border: none; width: 100%;
                box-shadow: 0 4px 12px rgba(242,101,34,0.3);
                transition: all 0.15s ease;
            }}
            div.stButton > button:hover {{ transform: translateY(-1px); box-shadow: 0 6px 16px rgba(242,101,34,0.4); }}

            /* Bouton secondaire — Nouveau commentaire */
            button[kind="secondary"] {{
                background: {BLANC} !important;
                color: {NOIR} !important;
                border: 1.5px solid #D0D0CC !important;
                box-shadow: none !important;
            }}
            button[kind="secondary"]:hover {{
                background: #F5F5F3 !important;
                border-color: {ORANGE} !important;
                color: {ORANGE} !important;
                transform: none !important;
            }}

            /* Bouton de téléchargement PDF / CSV */
            div.stDownloadButton > button {{
                background: linear-gradient(135deg, {ROUGE} 0%, {ROUGE_FONCE} 100%) !important;
                color: {BLANC} !important;
                font-weight: 700 !important;
                font-size: 15px !important;
                padding: 12px 26px !important;
                border-radius: 12px !important;
                border: none !important;
                width: 100% !important;
                box-shadow: 0 4px 12px rgba(193,39,45,0.3) !important;
            }}
            div.stDownloadButton > button:hover {{
                box-shadow: 0 6px 16px rgba(193,39,45,0.4) !important;
            }}

            /* Tuiles de résultat */
            .tile {{
                border-radius: 16px;
                padding: 20px 14px;
                text-align: center;
                box-shadow: 0 4px 14px rgba(0,0,0,0.12);
                min-height: 150px;
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                color: {BLANC};
            }}
            .tile-icon {{ margin-bottom: 8px; }}
            .tile-label {{ font-size: 10.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; opacity: 0.85; margin-bottom: 6px; }}
            .tile-value {{ font-size: 19px; font-weight: 800; margin-bottom: 4px; }}
            .tile-conf {{ font-size: 11.5px; opacity: 0.85; }}

            .tile-positif   {{ background: linear-gradient(135deg, {VERT_CLAIR} 0%, {VERT} 100%); }}
            .tile-neutre    {{ background: linear-gradient(135deg, {JAUNE} 0%, #B8860B 100%); }}
            .tile-negatif   {{ background: linear-gradient(135deg, {ROUGE} 0%, {ROUGE_FONCE} 100%); }}
            .tile-eleve     {{ background: linear-gradient(135deg, {ROUGE} 0%, {ROUGE_FONCE} 100%); }}
            .tile-moyen     {{ background: linear-gradient(135deg, {ORANGE_CLAIR} 0%, {ORANGE} 100%); }}
            .tile-faible    {{ background: linear-gradient(135deg, {VERT_CLAIR} 0%, {VERT} 100%); }}
            .tile-nonevalue {{ background: linear-gradient(135deg, #AFAFAF 0%, #888888 100%); }}

            /* Historique */
            .hist-row {{
                display: flex; align-items: center; justify-content: space-between;
                padding: 10px 4px; border-bottom: 1px solid {BORDURE};
                font-size: 13.5px;
            }}
            .hist-row:last-child {{ border-bottom: none; }}
            .hist-text {{ color: {NOIR}; max-width: 55%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
            .hist-badge {{
                font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 20px; color: white;
            }}
            .hist-time {{ color: {GRIS_TEXTE}; font-size: 11.5px; }}

            footer {{visibility: hidden;}}
            #MainMenu {{visibility: hidden;}}
        </style>
        """,
        unsafe_allow_html=True,
    )


def afficher_header():
    import os
    import base64
    from config import LOGO_PATH
    from icons import ICONS

    logo_html = ICONS["bank"]  # secours si le fichier logo n'est pas trouvé
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width:100%;height:100%;object-fit:contain;border-radius:8px;">'

    st.markdown(
        f"""
        <div class="aw-header">
            <div class="aw-logo">{logo_html}</div>
            <div class="aw-header-text">
                <h1>Attijari bank</h1>
                <p>Analyse intelligente des réclamations clients — Sentiment &amp; Risque de Churn</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def afficher_footer():
    st.markdown(
        f"""
        <div style="text-align:center; margin-top:8px; padding-top:14px; color:{GRIS_TEXTE}; font-size:11.5px;">
             Attijari bank · Analyse des réclamations clients 
        </div>
        """,
        unsafe_allow_html=True,
    )
