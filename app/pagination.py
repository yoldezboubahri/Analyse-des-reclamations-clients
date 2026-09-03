# -*- coding: utf-8 -*-
"""
pagination.py
-------------
Sélecteur de pages numérotées 
"""

import streamlit as st


def afficher_pagination(cle_page: str, total_lignes: int, taille_page: int = 10) -> int:
    """
    Affiche un sélecteur de pages numérotées  et renvoie
    l'index (0-based) de la page actuellement sélectionnée pour `cle_page`.
    """
    total_pages = max(1, (total_lignes - 1) // taille_page + 1)

    if cle_page not in st.session_state:
        st.session_state[cle_page] = 0
    if st.session_state[cle_page] > total_pages - 1:
        st.session_state[cle_page] = total_pages - 1
    if st.session_state[cle_page] < 0:
        st.session_state[cle_page] = 0

    page_actuelle = st.session_state[cle_page]

    if total_pages > 1:
        # Fenêtre de numéros de page affichés autour de la page courante
        fenetre = 5
        debut = max(0, min(page_actuelle - fenetre // 2, total_pages - fenetre))
        fin = min(total_pages, debut + fenetre)

        nb_boutons = 2 + (fin - debut)  # précédent + numéros + suivant
        cols = st.columns(nb_boutons)

        with cols[0]:
            if st.button("◀", key=f"{cle_page}_prev", disabled=(page_actuelle == 0), use_container_width=True):
                st.session_state[cle_page] = max(0, page_actuelle - 1)
                st.rerun()

        for i, num_page in enumerate(range(debut, fin)):
            with cols[1 + i]:
                est_active = (num_page == page_actuelle)
                if st.button(
                    str(num_page + 1),
                    key=f"{cle_page}_p{num_page}",
                    type="primary" if est_active else "secondary",
                    use_container_width=True,
                ):
                    st.session_state[cle_page] = num_page
                    st.rerun()

        with cols[-1]:
            if st.button("▶", key=f"{cle_page}_next", disabled=(page_actuelle == total_pages - 1), use_container_width=True):
                st.session_state[cle_page] = min(total_pages - 1, page_actuelle + 1)
                st.rerun()

        st.caption(f"Page {page_actuelle + 1} / {total_pages} — {total_lignes} ligne{'s' if total_lignes > 1 else ''} au total")

    return st.session_state[cle_page]
