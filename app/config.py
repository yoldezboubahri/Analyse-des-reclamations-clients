# -*- coding: utf-8 -*-
"""
config.py
---------
Constantes partagées par toute l'application : chemins des modèles,
device torch, palette de couleurs Attijari bank, et colonnes optionnelles
reconnues dans les fichiers importés.
"""

from pathlib import Path
import torch

# ------------------------------------------------------------------
# Chemins locaux 
# ------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
SENTIMENT_MODEL_DIR = BASE_DIR / "models" / "sentiment_xlmr"
CHURN_MODEL_DIR = BASE_DIR / "models" / "churnrisk_xlmr_negatif"
MAX_LENGTH = 128
SENTIMENT_LABEL_TRIGGER = "Négatif"

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Chemin du logo 
LOGO_PATH = "logo_attijari.png"

# ------------------------------------------------------------------
# Palette
# ------------------------------------------------------------------
ROUGE_FONCE = "#7A1B1E"
ROUGE = "#C1272D"
ORANGE = "#F26522"
ORANGE_CLAIR = "#F7941E"
JAUNE = "#F2A900"
NOIR = "#1A1A1A"
GRIS_FOND = "#F3F3F1"
GRIS_TEXTE = "#6B6B6B"
BLANC = "#FFFFFF"
VERT = "#2E7D32"
VERT_CLAIR = "#43A047"
BORDURE = "#E4E4E2"

# ------------------------------------------------------------------
# Colonnes optionnelles reconnues dans le fichier importé
# ( plusieurs variantes de nom acceptées)
# ------------------------------------------------------------------
CANDIDATS_COLONNES = {
    "ID_Client": ["ID_Client", "IdClient", "Client_ID", "ID Client", "id_client", "Identifiant_Client", "IDClient"],
    "Code_Motif": ["Code_Motif", "CodeMotif", "Motif", "Code Motif", "code_motif"],
    "Canal": ["Canal", "canal"],
    "Date_Contact": ["Date_Contact", "DateContact", "Date", "date_contact"],
    "langue": ["langue", "Langue", "language"],
}

# ------------------------------------------------------------------
# Couleurs des badges d'historique
# ------------------------------------------------------------------
BADGE_COLORS = {
    "Positif": "#2EC421", "Faible": "#2EC421",
    "Neutre": "#E4B640",
    "Négatif": "#E53941", "Élevé": "#E53941",
    "Moyen": "#F06428",
}
