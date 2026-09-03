# -*- coding: utf-8 -*-
"""
models.py
---------
Chargement des modèles (mis en cache par Streamlit) et fonction d'inférence
pour un texte unique.
"""

import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from config import SENTIMENT_MODEL_DIR, CHURN_MODEL_DIR, MAX_LENGTH, DEVICE


@st.cache_resource(show_spinner="Chargement des modèles...")
def load_pipeline():
    sent_tok = AutoTokenizer.from_pretrained(SENTIMENT_MODEL_DIR)
    sent_model = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL_DIR).to(DEVICE).eval()
    churn_tok = AutoTokenizer.from_pretrained(CHURN_MODEL_DIR)
    churn_model = AutoModelForSequenceClassification.from_pretrained(CHURN_MODEL_DIR).to(DEVICE).eval()
    return sent_tok, sent_model, churn_tok, churn_model


def predict_one(tokenizer, model, id2label, texte):
    inputs = tokenizer(texte, truncation=True, padding=True, max_length=MAX_LENGTH, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        logits = model(**inputs).logits
    probs = torch.softmax(logits, dim=-1)[0]
    pred_id = int(torch.argmax(probs).item())
    return id2label[pred_id], round(float(probs[pred_id]) * 100, 1)
