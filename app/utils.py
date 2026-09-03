# -*- coding: utf-8 -*-
"""
utils.py
--------
Petites fonctions utilitaires réutilisées à plusieurs endroits de l'app.
"""

import pandas as pd


def find_column(df: pd.DataFrame, candidats: list) -> str | None:
    """Retourne le nom réel de la colonne du df qui correspond à l'un des candidats (insensible à la casse)."""
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in candidats:
        if cand.lower() in cols_lower:
            return cols_lower[cand.lower()]
    return None


def clean_text(texte: str) -> str:
    return str(texte).strip()
