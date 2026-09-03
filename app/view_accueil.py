# -*- coding: utf-8 -*-
"""
view_accueil.py
----------------
Page "Accueil" : import du fichier de réclamations, lancement de l'analyse
par lot, aperçu statistique du dernier lot analysé.
"""

from datetime import datetime

import pandas as pd
import streamlit as st

from config import CANDIDATS_COLONNES, SENTIMENT_LABEL_TRIGGER
from icons import ICONS
from utils import find_column, clean_text
from models import predict_one
from pagination import afficher_pagination
from stats_view import afficher_stats


def render(sent_tok, sent_model, churn_tok, churn_model):
    # ------------------------------------------------------------------
    # Carte de saisie — upload d'un fichier (CSV / Excel / TXT)
    # ------------------------------------------------------------------
    st.markdown('<div class="aw-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="aw-card-title">{ICONS["search_dark"]} Fichier de réclamations</div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#6B6B6B; font-size:13px; margin-bottom:10px; margin-top:-6px;">'
        'Importez un fichier <b>.csv</b>, <b>.xlsx</b> ou <b>.txt</b> contenant les comptes-rendus clients. '
        'Pour un CSV/Excel.</p>',
        unsafe_allow_html=True,
    )

    fichier = st.file_uploader(
        "fichier_reclamations",
        type=["csv", "xlsx", "txt"],
        label_visibility="collapsed",
        key=f"fichier_{st.session_state.input_key}",
    )

    lignes_a_analyser = []
    colonne_choisie = None
    df_source = None

    if fichier is not None:
        extension = fichier.name.split(".")[-1].lower()

        if extension == "txt":
            contenu = fichier.read().decode("utf-8", errors="ignore")
            lignes_a_analyser = [l.strip() for l in contenu.split("\n") if l.strip()]
            st.success(f"{len(lignes_a_analyser)} réclamation(s) détectée(s) dans le fichier texte.")

        else:
            try:
                if extension == "csv":
                    df_upload = pd.read_csv(fichier)
                else:
                    df_upload = pd.read_excel(fichier)

                colonnes_candidates = ["clean_text_v2", "Compte_Rendu_Text", "texte", "commentaire", "reclamation"]
                defaut = next((c for c in colonnes_candidates if c in df_upload.columns), df_upload.columns[0])

                colonne_choisie = st.selectbox(
                    "Colonne contenant le texte de la réclamation :",
                    options=list(df_upload.columns),
                    index=list(df_upload.columns).index(defaut),
                )

                df_valid = df_upload.copy()
                df_valid[colonne_choisie] = df_valid[colonne_choisie].astype(str).str.strip()
                df_valid = df_valid[(df_valid[colonne_choisie] != "") & (df_valid[colonne_choisie].str.lower() != "nan")]
                df_valid.reset_index(drop=True, inplace=True)

                lignes_a_analyser = df_valid[colonne_choisie].tolist()
                df_source = df_valid

                st.success(f"{len(lignes_a_analyser)} réclamation(s) détectée(s) dans la colonne « {colonne_choisie} ».")

                # Aperçu des colonnes optionnelles détectées automatiquement (ID Client, Motif, etc.)
                colonnes_detectees = {cle: find_column(df_upload, cands) for cle, cands in CANDIDATS_COLONNES.items()}
                colonnes_detectees = {k: v for k, v in colonnes_detectees.items() if v}
                if colonnes_detectees:
                    detail = ", ".join(f"{k} → « {v} »" for k, v in colonnes_detectees.items())
                    st.caption(f"Colonnes reconnues automatiquement : {detail}")

                with st.expander("Aperçu du fichier"):
                    taille_page_apercu = 10
                    page_apercu = afficher_pagination("page_apercu_fichier", len(df_upload), taille_page_apercu)
                    debut_apercu = page_apercu * taille_page_apercu
                    fin_apercu = debut_apercu + taille_page_apercu
                    st.dataframe(df_upload.iloc[debut_apercu:fin_apercu], use_container_width=True)

            except Exception as e:
                st.error(f"Erreur de lecture du fichier : {e}")

    col_a, col_b = st.columns([2, 1])
    with col_a:
        analyser_clic = st.button("Analyser le fichier", type="primary", disabled=(fichier is None))
    with col_b:
        nouveau_clic = st.button("↺ Nouveau fichier", type="secondary")

    if nouveau_clic:
        st.session_state.input_key += 1
        st.session_state.tous_resultats = []
        st.session_state.df_stats = None
        st.session_state.historique = []
        st.session_state.page_detail_reclamations = 0
        st.session_state.page_apercu_fichier = 0
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # Résultats — boucle sur chaque réclamation du fichier
    # ------------------------------------------------------------------
    if analyser_clic:
        lignes = lignes_a_analyser

        if not lignes:
            st.warning("Aucune réclamation détectée dans le fichier.")
        else:
            resultats_batch = []
            progress = st.progress(0, text=f"Analyse de {len(lignes)} réclamation(s)...")

            for i, ligne in enumerate(lignes):
                texte = clean_text(ligne)
                sentiment, sent_conf = predict_one(sent_tok, sent_model, sent_model.config.id2label, texte)

                churn_risk, churn_conf = None, None
                if sentiment == SENTIMENT_LABEL_TRIGGER:
                    churn_risk, churn_conf = predict_one(churn_tok, churn_model, churn_model.config.id2label, texte)

                record = {
                    "texte": ligne,
                    "sentiment": sentiment,
                    "sent_conf": sent_conf,
                    "churn_risk": churn_risk,
                    "churn_conf": churn_conf,
                    "heure": datetime.now().strftime("%H:%M:%S"),
                }
                if df_source is not None:
                    for cle, candidats in CANDIDATS_COLONNES.items():
                        col = find_column(df_source, candidats)
                        if col:
                            record[cle] = df_source.iloc[i][col]

                resultats_batch.append(record)
                st.session_state.historique.insert(0, {
                    "texte": ligne[:60],
                    "sentiment": sentiment,
                    "churn_risk": churn_risk,
                    "heure": record["heure"],
                })
                progress.progress((i + 1) / len(lignes), text=f"Analyse {i + 1}/{len(lignes)}...")

            # Le PDF/CSV et la page Statistiques/Détails ne contiennent QUE le lot qui vient d'être analysé
            st.session_state.tous_resultats = resultats_batch
            st.session_state.df_stats = pd.DataFrame(resultats_batch)
            st.session_state.historique = st.session_state.historique[:5]
            st.session_state.page_detail_reclamations = 0
            st.session_state.page_liste_details = 0
            progress.empty()
            st.rerun()

    # ------------------------------------------------------------------
    # Résultat de l'analyse : aperçu statistique global, affiché ici
    # directement en dessous de l'import (dernier lot analysé)
    # ------------------------------------------------------------------
    afficher_stats(st.session_state.df_stats)
