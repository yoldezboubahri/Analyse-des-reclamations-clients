# -*- coding: utf-8 -*-
"""
exports.py
----------
Génération des exports du dernier lot analysé : rapport PDF (reportlab)
et export tabulaire CSV.
"""

import io
from datetime import datetime

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER


def generer_pdf(resultats):
    """
    Génère un PDF récapitulatif contenant TOUTES les analyses de la session.
    `resultats` : liste de dicts {texte, sentiment, sent_conf, churn_risk, churn_conf, heure, ID_Client, Code_Motif}
    Une section numérotée par analyse.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=20 * mm, bottomMargin=20 * mm,
        leftMargin=20 * mm, rightMargin=20 * mm,
    )

    styles = getSampleStyleSheet()
    style_titre = ParagraphStyle(
        "TitrePDF", parent=styles["Heading1"],
        fontSize=18, textColor=colors.HexColor("#7A1B1E"),
        alignment=TA_CENTER, spaceAfter=4,
    )
    style_sous_titre = ParagraphStyle(
        "SousTitrePDF", parent=styles["Normal"],
        fontSize=10, textColor=colors.HexColor("#6B6B6B"),
        alignment=TA_CENTER, spaceAfter=6,
    )
    style_compteur = ParagraphStyle(
        "CompteurPDF", parent=styles["Normal"],
        fontSize=9.5, textColor=colors.HexColor("#999999"),
        alignment=TA_CENTER, spaceAfter=20,
    )
    style_analyse_titre = ParagraphStyle(
        "AnalyseTitrePDF", parent=styles["Heading2"],
        fontSize=13, textColor=colors.HexColor("#C1272D"),
        spaceBefore=18, spaceAfter=8,
    )
    style_section = ParagraphStyle(
        "SectionPDF", parent=styles["Heading3"],
        fontSize=10.5, textColor=colors.HexColor("#1A1A1A"),
        spaceBefore=6, spaceAfter=6,
    )
    style_corps = ParagraphStyle(
        "CorpsPDF", parent=styles["Normal"],
        fontSize=10.5, textColor=colors.HexColor("#1A1A1A"),
        leading=15,
    )
    style_meta = ParagraphStyle(
        "MetaPDF", parent=styles["Normal"],
        fontSize=9.5, textColor=colors.HexColor("#6B6B6B"),
        spaceAfter=6,
    )
    style_tableau_titre = ParagraphStyle(
        "TableauTitrePDF", parent=styles["Heading2"],
        fontSize=12, textColor=colors.HexColor("#7A1B1E"),
        spaceBefore=4, spaceAfter=10,
    )

    n = len(resultats)
    elements = [
        Paragraph("Attijari bank", style_titre),
        Paragraph("Rapport d'analyse — Sentiment &amp; Risque de Churn", style_sous_titre),
        Paragraph(f"{n} réclamation{'s' if n > 1 else ''} analysée{'s' if n > 1 else ''}", style_compteur),
    ]

    couleurs_sentiment = {"Positif": "#2E7D32", "Neutre": "#B8860B", "Négatif": "#C1272D"}
    couleurs_churn = {"Élevé": "#C1272D", "Moyen": "#F26522", "Faible": "#2E7D32"}

    # ------------------------------------------------------------------
    # Tableau récapitulatif : ID Client, Date, Motif, Sentiment, Risque
    # ------------------------------------------------------------------
    elements.append(Paragraph("Tableau récapitulatif", style_tableau_titre))
    entete = ["ID Client", "Date", "Motif", "Sentiment", "Risque attrition"]
    lignes_tableau = [entete]
    for r in reversed(resultats):
        date_val = r.get("Date_Contact", "")
        lignes_tableau.append([
            str(r.get("ID_Client", "") or "—"),
            str(date_val) if date_val not in (None, "") else "—",
            str(r.get("Code_Motif", "") or "—"),
            r["sentiment"],
            r["churn_risk"] if r["churn_risk"] else "Pas de risque",
        ])

    style_cellule = ParagraphStyle("CelluleTableauPDF", parent=styles["Normal"], fontSize=8.5, leading=10)
    style_entete_cellule = ParagraphStyle("EnteteTableauPDF", parent=styles["Normal"], fontSize=8.5, leading=10, textColor=colors.white, fontName="Helvetica-Bold")
    lignes_tableau_p = [[Paragraph(str(c), style_entete_cellule) for c in entete]]
    for ligne in lignes_tableau[1:]:
        lignes_tableau_p.append([Paragraph(str(c), style_cellule) for c in ligne])

    tableau_recap = Table(lignes_tableau_p, colWidths=[70, 65, 90, 75, 90], repeatRows=1)
    style_commands = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#7A1B1E")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E0E0E0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FAFAF9")]),
    ]
    couleurs_risque_pdf = {"Élevé": "#C1272D", "Moyen": "#F26522", "Pas de risque": "#2E7D32"}
    colonne_risque_idx = entete.index("Risque attrition")
    for i, ligne in enumerate(lignes_tableau[1:], start=1):
        valeur_risque = ligne[colonne_risque_idx]
        if valeur_risque in couleurs_risque_pdf:
            style_commands.append((
                "BACKGROUND", (colonne_risque_idx, i), (colonne_risque_idx, i),
                colors.HexColor(couleurs_risque_pdf[valeur_risque]),
            ))
            style_commands.append((
                "TEXTCOLOR", (colonne_risque_idx, i), (colonne_risque_idx, i), colors.white,
            ))
    tableau_recap.setStyle(TableStyle(style_commands))
    elements.append(tableau_recap)
    elements.append(Spacer(1, 14))
    elements.append(Paragraph(
        f"Document généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} — "
        "Aiijari bank · Analyse des réclamations clients",
        ParagraphStyle("Footer", parent=styles["Normal"], fontSize=8, textColor=colors.HexColor("#999999")),
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def generer_csv(resultats):
    """
    Génère un export tabulaire (CSV) avec, pour chaque compte-rendu analysé :
    ID Client, Date, Code Motif (si présents dans le fichier importé), Sentiment, Risque d'attrition.
    """
    lignes = []
    for r in resultats:
        lignes.append({
            "ID_Client": r.get("ID_Client", ""),
            "Date": r.get("Date_Contact", ""),
            "Code_Motif": r.get("Code_Motif", ""),
            "Sentiment": r["sentiment"],
            "Risque_Attrition": r["churn_risk"] if r["churn_risk"] else "Pas de risque",
        })
    df_export = pd.DataFrame(lignes)
    return df_export.to_csv(index=False).encode("utf-8-sig")
