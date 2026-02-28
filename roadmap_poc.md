# 🗺️ Plan PoC — brezhoneg-validation

> Objectif PoC (PRD §4.1) : **valider le concept** avec l'équipe de recherche.

---

## État actuel du projet

| Composant | État | Détails |
|-----------|------|---------|
| **Modèles SQLAlchemy** | ✅ Fait | `Segment`, `User`, `Annotation` — conforme au schéma PRD §7.3 |
| **Base SQLite** | ✅ Fait | Créée automatiquement dans `data/brezhoneg.db` |
| **Frontend** | ✅ Bootstrap | Vue 3 + Vite + Tailwind v4 — page d'accueil + test API |
| **Backend** | ✅ Bootstrap | FastAPI — `GET /api/hello` uniquement |
| **Vue Router** | ❌ Absent | Pas de routing côté client |
| **Scripts import/export** | ❌ Absent | Aucun fichier JSONL, aucun script |
| **Routes API** | ❌ Absent | Pas de routes users / segments / annotations |
| **Tests** | ❌ Absent | Aucun test unitaire ou d'intégration |

---

## Étapes PoC

### Étape 1 — Fondations backend (API + Import)

**But** : rendre le backend fonctionnel avec données et routes.

| Fichier | Action | Description |
|---------|--------|-------------|
| `backend/app/schemas.py` | **[NEW]** | Schémas Pydantic (UserCreate, UserOut, AnnotationCreate, AnnotationOut, SegmentOut) |
| `backend/app/routes/users.py` | **[NEW]** | `POST /api/users` (création profil), `GET /api/users/{id}` |
| `backend/app/routes/segments.py` | **[NEW]** | `GET /api/segments/next?user_id=…&source=…` (paire non annotée), `GET /api/segments/sources` (liste des corpus) |
| `backend/app/routes/annotations.py` | **[NEW]** | `POST /api/annotations` (soumettre), contrainte UNIQUE user×segment |
| `backend/app/routes/export.py` | **[NEW]** | `GET /api/export?format=jsonl\|csv` |
| `backend/app/main.py` | **[MODIFY]** | Enregistrer les routeurs, ajouter le dependency `get_db` |
| `backend/app/database.py` | **[MODIFY]** | Ajouter une factory `get_db()` pour l'injection de dépendances FastAPI |
| `scripts/import_corpus.py` | **[NEW]** | Script CLI : lire un `.jsonl`, insérer dans `segments` avec champ `source` |
| `data/` | — | Y placer un corpus JSONL de test (à fournir par l'utilisateur) |

---

### Étape 2 — Page profil utilisateur (F02)

**But** : permettre au locuteur de s'identifier au premier accès.

| Fichier | Action | Description |
|---------|--------|-------------|
| `frontend/src/views/ProfilView.vue` | **[NEW]** | Formulaire : pseudo, email, niveau, nom, prénom, genre, âge |
| `frontend/src/views/AnnotationView.vue` | **[NEW]** | Vue stub (sera remplie étape 3) |
| `frontend/src/router.js` | **[NEW]** | Vue Router : `/profil`, `/annotation` |
| `frontend/src/composables/useUser.js` | **[NEW]** | Composable simple : `userId` réactif + `localStorage` (pas de Pinia) |
| `frontend/src/main.js` | **[MODIFY]** | Importer le routeur |
| `frontend/src/App.vue` | **[MODIFY]** | Ajouter `<router-view>`, rediriger vers `/profil` si pas de profil |
| `frontend/package.json` | **[MODIFY]** | Ajouter `vue-router` |

---

### Étape 3 — Interface d'annotation (F03–F07)

**But** : cœur de l'application — annoter une paire par les 3 icônes.

| Fichier | Action | Description |
|---------|--------|-------------|
| `frontend/src/views/AnnotationView.vue` | **[MODIFY]** | Afficher paire br·fr, 3 boutons icônes ✅❌❓, champ correction optionnel, confiance conditionnelle (1–5) |
| `frontend/src/components/AnnotationCard.vue` | **[NEW]** | Composant carte : phrase breton + français |
| `frontend/src/components/AnnotationActions.vue` | **[NEW]** | Composant boutons d'annotation |
| `frontend/src/composables/useAnnotation.js` | **[NEW]** | Composable : segment courant, soumission, compteur |

---

### Étape 4 — Progression + Sélection corpus (F08–F09)

**But** : suivi visuel de l'avancement et filtrage par corpus source.

| Fichier | Action | Description |
|---------|--------|-------------|
| `frontend/src/components/ProgressBar.vue` | **[NEW]** | Compteur (session / total) + barre de progression |
| `frontend/src/views/AnnotationView.vue` | **[MODIFY]** | Intégrer la barre de progression, menu déroulant de sélection corpus |

---

### Étape 5 — Export annotations (F10)

**But** : permettre au chercheur de télécharger les annotations.

| Fichier | Action | Description |
|---------|--------|-------------|
| `backend/app/routes/export.py` | **[MODIFY]** | Implémenter `GET /api/export?format=jsonl` et `GET /api/export?format=csv` |

> **Note** : cette route existe déjà dans l'étape 1 comme stub ; ici on implémente la logique complète.

---

## Vérification

### Tests manuels (par étape)

1. **Étape 1** : Importer un JSONL de test → vérifier via `/docs` que les routes `GET /api/segments/next` et `POST /api/users` fonctionnent
2. **Étape 2** : Ouvrir `localhost:5173` → remplir le profil → vérifier que l'utilisateur est créé en base
3. **Étape 3** : Annoter 3-4 paires → vérifier que les annotations apparaissent en base, tester la contrainte UNIQUE
4. **Étape 4** : Vérifier que la barre de progression se met à jour après chaque annotation
5. **Étape 5** : Télécharger l'export JSONL et CSV → vérifier le contenu

### Critères de succès PoC

- ≥ 5 annotateurs actifs
- ≥ 500 annotations
- ≥ 20 % de couverture du corpus

---

## Dépendances à installer

| Package | Couche | Commande |
|---------|--------|----------|
| `pydantic` | Backend | Déjà inclus avec FastAPI |
| `vue-router` | Frontend | `npm install vue-router@4` |
| `lucide-vue-next` | Frontend | `npm install lucide-vue-next` — pour les icônes ✅❌❓ |
