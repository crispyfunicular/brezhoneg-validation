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

# Installer les dépendances
pip install -r backend/requirements.txt
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
├── data/                    # Données & base SQLite (gitignored)
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
