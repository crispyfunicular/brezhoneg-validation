# brezhoneg-validation

Plateforme de validation collaborative du corpus parallèle breton–français.

> **Projet Korpusou / MoDyCo — Licence MIT**

---

## Prérequis

| Outil | Version minimale |
|-------|-----------------|
| Python | 3.11+ |
| Node.js | 20+ |
| npm | 9+ |

---

## Installation

### 1. Backend (Python / FastAPI)

```bash
# Créer et activer le venv
python3 -m venv .venv
source .venv/bin/activate

# Installer le projet en mode développement
pip install -e .
```

### 2. Frontend (Vue 3 / Vite / Tailwind CSS)

```bash
cd frontend
npm install
```

---

## Lancement

### Mode développement (deux terminaux, hot-reload)

```bash
# Terminal 1 — Backend (port 8000)
source .venv/bin/activate
uvicorn backend.app.main:app --reload --port 8000

# Terminal 2 — Frontend (port 5173)
cd frontend
npm run dev
```

Ouvrir `http://localhost:5173`. Les appels `/api/*` sont automatiquement proxifiés vers le backend par Vite.

Documentation API auto-générée : `http://localhost:8000/docs`.

### Mode production (serveur unique)

```bash
# 1. Build du frontend
cd frontend
npm run build        # → génère frontend/dist/

# 2. Lancer le backend (sert aussi le frontend)
cd ..
source .venv/bin/activate
uvicorn backend.app.main:app --port 8000
```

Tout est servi sur `http://localhost:8000` — API et interface.

---

## Import de corpus

Importer un fichier JSONL dans la table `segments` :

```bash
source .venv/bin/activate
python scripts/import_corpus.py data/arbres-kenstur.jsonl
```

```bash
sqlite3 data/brezhoneg.db
SQLite version 3.45.1 2024-01-30 16:01:20
Enter ".help" for usage hints.
sqlite> SELECT * FROM segments;
1|"Alo, amañ Lizig ! A, Mari, te an hini eo ?"|"Allo, ici Lizig ! Ah, Marie, c'est toi ?"|arbres-kenstur|2026-03-03 07:46:36.159307
2|"Amiguito", ha n'oc'h eus ket lavaret din ne vezoc'h gant ho servij en iliz nemet e-pad ur sizhunvezh ?|Amiguito, ne m'avez-vous pas dit que vous serez de service à l'église pendant seulement une semaine ?|arbres-kenstur|2026-03-03 07:46:36.159312
3|"Emañ lipet ganti he loa!" eme Brimel neuze.|Brimel dit alors "Elle est morte !"|arbres-kenstur|2026-03-03 07:46:36.159313

sqlite> SELECT * FROM segments WHERE francais LIKE '%demain%';
178|A-benn arhoaz d'an eur-mañ e vint o labourad da vad.|Demain à cette heure-ci, ils seront en plein travail.|arbres-kenstur|2026-03-03 07:46:36.159429
474|An den a zo hirio; warc'hoazh n'ema mui !|L'homme existe aujourd'hui, demain il ne sera plus !|arbres-kenstur|2026-03-03 07:46:36.159653
476|An dervez war-lerc'h, houman a gane war ar reier, penfollet.|Le lendemain, elle chantait sur les rochers, égarée.|arbres-kenstur|2026-03-03 07:46:36.159654
```


Le nom de la source est déduit du fichier (`arbres-kenstur`), ou peut être précisé avec `--source "mon_corpus"`.

Format JSONL attendu (un objet par ligne) :

```json
{"translation": {"br": "Demat", "fr": "Bonjour"}}
```

Pour réimporter un corpus (supprime puis réinsère les segments de cette source) :

```bash
python scripts/import_corpus.py data/arbres-kenstur.jsonl --replace
```

---

## Structure du projet

```
brezhoneg-validation/
├── backend/                 # API — Python / FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # Point d'entrée FastAPI
│   │   ├── database.py      # Engine SQLAlchemy + session
│   │   └── models.py        # Modèles : Segment, User, Annotation
│   └── requirements.txt
├── frontend/                # Client — Vue 3 / Vite / Tailwind CSS
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── scripts/                 # Scripts utilitaires
│   └── import_corpus.py     # Import JSONL → table segments
├── data/                    # Données & base SQLite (gitignored)
├── pyproject.toml           # Configuration projet Python
├── .gitignore
├── LICENSE
├── PRD.md
└── README.md
```

---

## Base de données

Au démarrage, le backend crée automatiquement la base SQLite `data/brezhoneg.db` avec les tables :

- **segments** — paires breton / français
- **users** — profils annotateurs
- **annotations** — labels, corrections, confiance
