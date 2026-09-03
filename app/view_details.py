# -*- coding: utf-8 -*-
"""
view_details.py
-----------------
Page "Détails" : export PDF/CSV du dernier lot, et tableau détaillé
paginé + filtrable par sentiment / risque d'attrition.
"""

from datetime import datetime

import streamlit as st

from config import ROUGE, ORANGE, VERT, NOIR, GRIS_TEXTE
from icons import ICONS
from exports import generer_pdf, generer_csv
from pagination import afficher_pagination


def render():
    if not st.session_state.tous_resultats:
        st.markdown(
            f"""
            <div class="aw-card" style="text-align:center; padding:50px 28px;">
                <div style="margin-bottom:14px;">{ICONS["search_dark"]}</div>
                <div style="font-size:16px; font-weight:700; color:{NOIR}; margin-bottom:8px;">
                    Aucun compte-rendu à afficher
                </div>
                <div style="font-size:13.5px; color:{GRIS_TEXTE};">
                    Importez et analysez un fichier depuis l'onglet <b>Accueil</b> pour voir le détail ici.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    resultats_batch = st.session_state.tous_resultats
    n_analyses = len(resultats_batch)

    # --- Export : PDF ou CSV (en haut, visible sans scroller) ---
    st.markdown('<div class="aw-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="aw-card-title">{ICONS["check_dark"]} Exporter le rapport</div>', unsafe_allow_html=True)
    st.markdown(
        f'<p style="color:#6B6B6B; font-size:13.5px; margin-bottom:14px;">'
        f'Téléchargez les résultats des {n_analyses} réclamation{"s" if n_analyses > 1 else ""} '
        f'du dernier lot analysé.</p>',
        unsafe_allow_html=True,
    )

    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")

    exp_col1, exp_col2 = st.columns(2)
    with exp_col1:
        pdf_buffer = generer_pdf(resultats_batch)
        st.download_button(
            label=f"⬇ Rapport PDF ({n_analyses})",
            data=pdf_buffer,
            file_name=f"rapport_analyses_{n_analyses}_{horodatage}.pdf",
            mime="application/pdf",
        )
    with exp_col2:
        csv_buffer = generer_csv(resultats_batch)
        st.download_button(
            label=f"⬇ Export CSV ({n_analyses})",
            data=csv_buffer,
            file_name=f"export_analyses_{n_analyses}_{horodatage}.csv",
            mime="text/csv",
        )

    st.caption("PDF et CSV contiennent tous deux : ID Client, Date, Code Motif (si détectés), Sentiment, Risque d'attrition.")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Détail des réclamations (tableau paginé : 10 lignes par page) ---
    st.markdown('<div class="aw-card">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="aw-card-title">{ICONS["check_dark"]} Détail des réclamations — {len(resultats_batch)} réclamation'
        f'{"s" if len(resultats_batch) > 1 else ""} analysée{"s" if len(resultats_batch) > 1 else ""}</div>',
        unsafe_allow_html=True,
    )

    df_detail = st.session_state.df_stats.copy()
    if "churn_risk" in df_detail.columns:
        df_detail["churn_risk"] = df_detail["churn_risk"].fillna("Pas de risque")
    colonnes_affichees = [c for c in ["ID_Client", "Canal", "Code_Motif", "texte", "sentiment", "sent_conf", "churn_risk", "churn_conf", "langue"] if c in df_detail.columns]

    # --- Filtres Sentiment / Risque ---
    filtre_col1, filtre_col2 = st.columns(2)
    with filtre_col1:
        options_sentiment = [o for o in ["Positif", "Neutre", "Négatif"] if o in df_detail["sentiment"].unique()]
        filtre_sentiment = st.multiselect(
            "Filtrer par sentiment",
            options=options_sentiment,
            default=options_sentiment,
            key="filtre_sentiment_detail",
        )
    with filtre_col2:
        options_risque = [o for o in ["Élevé", "Moyen"] if o in df_detail["churn_risk"].unique()]
        filtre_risque = st.multiselect(
            "Filtrer par risque d'attrition",
            options=options_risque,
            default=options_risque,
            key="filtre_risque_detail",
        )

    df_detail = df_detail[
        df_detail["sentiment"].isin(filtre_sentiment)
        & (df_detail["churn_risk"].isin(filtre_risque) | (~df_detail["churn_risk"].isin(["Élevé", "Moyen"])))
    ]

    if df_detail.empty:
        st.info("Aucune réclamation ne correspond aux filtres sélectionnés.")
    else:
        taille_page_detail = 10
        page_detail = afficher_pagination("page_detail_reclamations", len(df_detail), taille_page_detail)
        debut_detail = page_detail * taille_page_detail
        fin_detail = debut_detail + taille_page_detail

        def _couleur_risque(val):
            if val == "Élevé":
                return f"background-color: {ROUGE}; color: white"
            if val == "Moyen":
                return f"background-color: {ORANGE}; color: white"
            if val == "Pas de risque":
                return f"background-color: {VERT}; color: white"
            return ""

        df_page = df_detail[colonnes_affichees].iloc[debut_detail:fin_detail]
        if "churn_risk" in df_page.columns:
            styler = df_page.style
            try:
                df_page_style = styler.map(_couleur_risque, subset=["churn_risk"])
            except AttributeError:
                df_page_style = styler.applymap(_couleur_risque, subset=["churn_risk"])
            st.dataframe(df_page_style, use_container_width=True, height=280)
        else:
            st.dataframe(df_page, use_container_width=True, height=280)

    st.markdown('</div>', unsafe_allow_html=True)
