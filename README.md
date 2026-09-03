# Attijari bank — Analyse Client (Sentiment & Risque de Churn)

Application Streamlit d'analyse de réclamations clients multilingues (français, arabe et en dialecte tunisien) : classification du sentiment et estimation du risque d'attrition (churn), via un pipeline en cascade de deux modèles XLM-RoBERTa fine-tunés.


## Structure du projet

```
text_mining/
├── app/                    # Application Streamlit (voir app/ ci-dessous)
├── data/                   # Données 
│   ├── raw/
│   └── processed/
├── models/                 
│   ├── sentiment_xlmr/
│   └── churnrisk_xlmr_negatif/
├── notebooks/               # Pipeline complet : nettoyage, labeling, split, fine-tuning
├── requirements.txt
└── README.md
```

### `app/`

| Fichier              | Rôle                                                        |
|----------------------|--------------------------------------------------------------|
| `app.py`             | Point d'entrée — orchestration, navigation, session state    |
| `config.py`          | Chemins, device, palette de couleurs, colonnes reconnues     |
| `utils.py`           | Fonctions utilitaires (détection de colonnes, nettoyage)     |
| `models.py`          | Chargement des modèles et inférence                          |
| `icons.py`           | Icônes SVG                                                    |
| `styles.py`          | CSS + en-tête / pied de page                                  |
| `pagination.py`      | Composant de pagination réutilisable                          |
| `exports.py`         | Génération des rapports PDF / CSV                             |
| `stats_view.py`      | Graphiques et KPIs                                             |
| `view_accueil.py`    | Page d'import et d'analyse par lot                             |
| `view_details.py`    | Page de détail, filtres et export                              |
| `logo_attijari.png`  | Logo affiché dans l'en-tête                                    |

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/yoldezboubahri/Analyse-des-reclamations-clients
cd Analyse-des-reclamations-clients
```

### 2. Créer l'environnement

Avec conda (recommandé, environnement utilisé pour le développement) :

```bash
conda create -n text python=3.11
conda activate text
pip install -r requirements.txt
```

Ou avec `venv` :

```bash
python -m venv venv
source venv/bin/activate   # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

> **GPU (optionnel) :** `pip install -r requirements.txt` installe une version CPU de PyTorch. Pour l'accélération GPU, installe d'abord `torch` selon ta configuration CUDA via [pytorch.org/get-started](https://pytorch.org/get-started/locally/), puis le reste des dépendances.

### 3. Télécharger les modèles

Les poids fine-tunés (~1.1 Go chacun) ne sont pas versionnés sur Git. Télécharge les deux archives depuis Google Drive :

- **Modèle Sentiment (XLM-R)** : `< https://drive.google.com/file/d/1MH71BEcOo3M6TKGshQKL5oX0H-Xsa0OP/view?usp=drive_link >` → `sentiment_xlmr.zip`
- **Modèle Churn Risk (XLM-R)** : `< https://drive.google.com/file/d/1OSKcz2F_TZbheifL0KPBjDYa2tHwlWmB/view?usp=drive_link >` → `churnrisk_xlmr_negatif.zip`

Puis extrais-les à la racine du projet, dans `models/`, de façon à obtenir exactement cette arborescence (4 fichiers par modèle, sans sous-dossier `checkpoint-*` ni `training_args.bin`) :

```
text_mining/
└── models/
    ├── sentiment_xlmr/
    │   ├── config.json
    │   ├── model.safetensors
    │   ├── tokenizer.json
    │   └── tokenizer_config.json
    └── churnrisk_xlmr_negatif/
        ├── config.json
        ├── model.safetensors
        ├── tokenizer.json
        └── tokenizer_config.json
```

**Windows (PowerShell)** — depuis la racine `text_mining/`, après avoir téléchargé les deux zips dans `Downloads` :

```powershell
Expand-Archive -Path "$HOME\Downloads\sentiment_xlmr.zip" -DestinationPath "models\sentiment_xlmr"
Expand-Archive -Path "$HOME\Downloads\churnrisk_xlmr_negatif.zip" -DestinationPath "models\churnrisk_xlmr_negatif"
```

**macOS / Linux** :

```bash
unzip ~/Downloads/sentiment_xlmr.zip -d models/sentiment_xlmr
unzip ~/Downloads/churnrisk_xlmr_negatif.zip -d models/churnrisk_xlmr_negatif
```

Vérifie ensuite que chaque dossier contient bien les 4 fichiers listés ci-dessus :

```powershell
dir models\sentiment_xlmr
dir models\churnrisk_xlmr_negatif
```

Si l'archive s'est extraite dans un sous-dossier imbriqué (ex. `models\sentiment_xlmr\sentiment_xlmr\config.json`), déplace les fichiers d'un niveau au-dessus pour que `config.json` et `model.safetensors` soient directement dans `models\sentiment_xlmr\`.

### 4. Lancer l'application

```bash
conda activate text
cd Analyse-des-reclamations-clients
cd app
python -m streamlit run app.py
```

L'application s'ouvre sur `http://localhost:8501`.

## Utilisation

1. Sur la page **Accueil**, importe un fichier `.csv`, `.xlsx` ou `.txt` contenant les comptes-rendus clients.
2. Sélectionne la colonne texte (détection automatique si le fichier suit un format connu).
3. Clique sur **Analyser le fichier** — chaque ligne passe par le modèle de sentiment, puis par le modèle de risque de churn si le sentiment est négatif.
4. Consulte les statistiques (KPIs, évolution temporelle, répartition par canal, motifs à risque) directement sous l'import.
5. Sur la page **Détails**, filtre les résultats et exporte le rapport en **PDF** ou **CSV**.

### Colonnes optionnelles reconnues automatiquement

Si présentes dans le fichier importé (sous plusieurs variantes de nom), ces colonnes enrichissent l'analyse et les exports :

- `ID_Client`
- `Code_Motif`
- `Canal`
- `Date_Contact`
- `langue`

## Pipeline de fine-tuning (notebooks/)

Le dossier `notebooks/` documente le pipeline complet, du nettoyage brut au fine-tuning :

1. `01_exploration_nettoyage.ipynb` — nettoyage multi-étapes et détection de langue
2. `02_creation_des_variables_cibles.ipynb` — labeling pour Sentiment et Churn Risk
3. `03_split_train_val_test.ipynb` — split stratifié par groupe (`template_id`) pour éviter les fuites de données
4. `04_finetuning_sentiments.ipynb` — fine-tuning complet de XLM-RoBERTa-base (sentiment)
5. `05_finetuning_churnrisks.ipynb` — fine-tuning du modèle de risque de churn (sous-ensemble Négatif)

Ces notebooks nécessitent le corpus source (non fourni dans ce dépôt public) pour être ré-exécutés.


