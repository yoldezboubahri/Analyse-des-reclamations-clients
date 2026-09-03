# -*- coding: utf-8 -*-
"""
stats_view.py
-------------
Section Statistiques : KPIs et graphiques (matplotlib) pour le dernier lot analysé.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from config import ROUGE, ROUGE_FONCE, ORANGE, ORANGE_CLAIR, JAUNE, NOIR, VERT_CLAIR
from icons import ICONS


def afficher_stats(df):
    """Affiche la section Statistiques (KPIs + graphiques) pour le DataFrame donné.
    N'affiche rien tant qu'aucune donnée n'a été analysée."""
    if df is None or df.empty:
        return
    else:
        total = len(df)
        n_negatif = (df["sentiment"] == "Négatif").sum()
        n_positif = (df["sentiment"] == "Positif").sum()
        n_neutre = (df["sentiment"] == "Neutre").sum()
        n_eleve = (df["churn_risk"] == "Élevé").sum()
        n_moyen = (df["churn_risk"] == "Moyen").sum()

        # --- KPIs ---
        st.markdown('<div class="aw-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="aw-card-title">{ICONS["check_dark"]} Vue d\'ensemble</div>', unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total analysé", total)
        k2.metric("% Négatif", f"{n_negatif / total * 100:.1f}%" if total else "—")
        k3.metric("Risque Élevé", n_eleve)
        k4.metric("Risque Moyen", n_moyen)
        st.markdown('</div>', unsafe_allow_html=True)

        # --- Évolution temporelle du % Négatif (si la colonne existe) ---
        if "Date_Contact" in df.columns:
            st.markdown('<div class="aw-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="aw-card-title">{ICONS["check_dark"]} Évolution du % Négatif dans le temps</div>', unsafe_allow_html=True)
            try:
                df_temps = df.copy()
                df_temps["Date_Contact"] = pd.to_datetime(df_temps["Date_Contact"], errors="coerce")
                df_temps = df_temps.dropna(subset=["Date_Contact"])

                if not df_temps.empty:
                    etendue_jours = (df_temps["Date_Contact"].max() - df_temps["Date_Contact"].min()).days
                    frequence = "D" if etendue_jours <= 31 else "W"
                    serie = df_temps.set_index("Date_Contact").resample(frequence)["sentiment"].apply(
                        lambda s: (s == "Négatif").mean() * 100 if len(s) > 0 else None
                    ).dropna()

                    if len(serie) >= 2:
                        fig_t, ax_t = plt.subplots(figsize=(6.4, 3))
                        ax_t.plot(serie.index, serie.values, color=ROUGE, marker="o", markersize=4, linewidth=2)
                        ax_t.fill_between(serie.index, serie.values, color=ROUGE, alpha=0.08)
                        ax_t.set_ylabel("% Négatif", fontsize=9)
                        ax_t.tick_params(labelsize=8, axis="x", rotation=25)
                        ax_t.tick_params(labelsize=9, axis="y")
                        for spine in ["top", "right"]:
                            ax_t.spines[spine].set_visible(False)
                        fig_t.patch.set_alpha(0)
                        fig_t.tight_layout()
                        st.pyplot(fig_t, use_container_width=True)
                    else:
                        st.info("Période trop courte pour afficher une évolution.")
                else:
                    st.info("Aucune date exploitable dans ce lot.")
            except Exception:
                st.info("Impossible d'interpréter la colonne de date pour ce lot.")
            st.markdown('</div>', unsafe_allow_html=True)

        # --- Répartition Sentiment (camembert) + Churn (barres) ---
        st.markdown('<div class="aw-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="aw-card-title">{ICONS["check_dark"]} Résultats des 2 modèles</div>', unsafe_allow_html=True)

        col_g, col_d = st.columns(2)

        with col_g:
            st.markdown("**Répartition par sentiment**")
            labels_s = ["Positif", "Neutre", "Négatif"]
            valeurs_s = [n_positif, n_neutre, n_negatif]
            couleurs_s = [VERT_CLAIR, JAUNE, ROUGE]
            labels_s_f = [l for l, v in zip(labels_s, valeurs_s) if v > 0]
            valeurs_s_f = [v for v in valeurs_s if v > 0]
            couleurs_s_f = [c for c, v in zip(couleurs_s, valeurs_s) if v > 0]

            if valeurs_s_f:
                fig1, ax1 = plt.subplots(figsize=(3.2, 3.2))
                ax1.pie(valeurs_s_f, labels=labels_s_f, colors=couleurs_s_f, autopct="%1.0f%%",
                        textprops={"fontsize": 9, "color": NOIR}, startangle=90)
                ax1.axis("equal")
                fig1.patch.set_alpha(0)
                st.pyplot(fig1, use_container_width=True)

        with col_d:
            st.markdown("**Risque (parmi les Négatifs)**")
            labels_c = ["Élevé", "Moyen"]
            valeurs_c = [n_eleve, n_moyen]
            couleurs_c = [ROUGE, ORANGE]

            if n_negatif > 0:
                fig2, ax2 = plt.subplots(figsize=(3.2, 3.2))
                ax2.bar(labels_c, valeurs_c, color=couleurs_c)
                ax2.set_ylabel("Nombre de réclamations", fontsize=8)
                ax2.tick_params(labelsize=9)
                for spine in ["top", "right"]:
                    ax2.spines[spine].set_visible(False)
                fig2.patch.set_alpha(0)
                st.pyplot(fig2, use_container_width=True)
            else:
                st.info("Aucune réclamation négative dans ce lot.")

        st.markdown('</div>', unsafe_allow_html=True)

        # --- Par canal (si la colonne existe) ---
        if "Canal" in df.columns:
            st.markdown('<div class="aw-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="aw-card-title">{ICONS["check_dark"]} Réclamations par canal</div>', unsafe_allow_html=True)

            col_c1, col_c2 = st.columns(2)

            with col_c1:
                st.markdown("**Volume par canal**")
                volume_canal = df["Canal"].value_counts()
                fig5b, ax5b = plt.subplots(figsize=(3.2, 3.2))
                ax5b.bar(volume_canal.index, volume_canal.values, color=ORANGE_CLAIR)
                ax5b.set_ylabel("Nombre de réclamations", fontsize=8)
                ax5b.tick_params(labelsize=9, axis="x", rotation=20)
                ax5b.tick_params(labelsize=9, axis="y")
                for spine in ["top", "right"]:
                    ax5b.spines[spine].set_visible(False)
                fig5b.patch.set_alpha(0)
                st.pyplot(fig5b, use_container_width=True)

            with col_c2:
                st.markdown("**% Négatif par canal**")
                pct_neg_canal = df.groupby("Canal")["sentiment"].apply(lambda s: (s == "Négatif").mean() * 100)
                fig5, ax5 = plt.subplots(figsize=(3.2, 3.2))
                ax5.bar(pct_neg_canal.index, pct_neg_canal.values, color=ROUGE_FONCE)
                ax5.set_ylabel("% Négatif", fontsize=8)
                ax5.tick_params(labelsize=9, axis="x", rotation=20)
                ax5.tick_params(labelsize=9, axis="y")
                for spine in ["top", "right"]:
                    ax5.spines[spine].set_visible(False)
                fig5.patch.set_alpha(0)
                st.pyplot(fig5, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

        # --- Croisement Canal x Motif (si les 2 colonnes existent) ---
        if "Canal" in df.columns and "Code_Motif" in df.columns:
            st.markdown('<div class="aw-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="aw-card-title">{ICONS["check_dark"]} Répartition des motifs par canal</div>', unsafe_allow_html=True)
            croisement = pd.crosstab(df["Code_Motif"], df["Canal"])
            if not croisement.empty:
                fig_heat, ax_heat = plt.subplots(figsize=(6.4, 3.6))
                im = ax_heat.imshow(croisement.values, cmap="Reds", aspect="auto")
                ax_heat.set_xticks(range(len(croisement.columns)))
                ax_heat.set_xticklabels(croisement.columns, fontsize=8, rotation=20)
                ax_heat.set_yticks(range(len(croisement.index)))
                ax_heat.set_yticklabels(croisement.index, fontsize=8)
                for i in range(len(croisement.index)):
                    for j in range(len(croisement.columns)):
                        valeur = croisement.values[i, j]
                        couleur_texte = "white" if valeur > croisement.values.max() / 2 else NOIR
                        ax_heat.text(j, i, valeur, ha="center", va="center", fontsize=8, color=couleur_texte)
                cbar = fig_heat.colorbar(im, ax=ax_heat, shrink=0.8)
                cbar.ax.tick_params(labelsize=8)
                fig_heat.patch.set_alpha(0)
                fig_heat.tight_layout()
                st.pyplot(fig_heat, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # --- Top motifs à risque (si la colonne existe) ---
        if "Code_Motif" in df.columns and n_negatif > 0:
            st.markdown('<div class="aw-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="aw-card-title">{ICONS["check_dark"]} Motifs les plus associés au risque Élevé</div>', unsafe_allow_html=True)
            df_negatif = df[df["sentiment"] == "Négatif"]
            top_motifs = df_negatif[df_negatif["churn_risk"] == "Élevé"]["Code_Motif"].value_counts().head(8)
            if not top_motifs.empty:
                fig6, ax6 = plt.subplots(figsize=(6.4, 3.2))
                ax6.barh(top_motifs.index[::-1], top_motifs.values[::-1], color=ROUGE)
                ax6.tick_params(labelsize=9)
                for spine in ["top", "right"]:
                    ax6.spines[spine].set_visible(False)
                fig6.patch.set_alpha(0)
                st.pyplot(fig6, use_container_width=True)
            else:
                st.info("Aucun motif à risque Élevé dans ce lot.")
            st.markdown('</div>', unsafe_allow_html=True)
