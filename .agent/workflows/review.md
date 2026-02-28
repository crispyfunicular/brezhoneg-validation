---
description: Revue critique des modifications locales non committées (revue de diff git)
---

# Revue des modifications locales

Revue approfondie et critique des modifications git locales — simulant une code review d'ingénieur senior.

RÈGLE CRITIQUE : NE JAMAIS effectuer d'action d'écriture sur GitHub sans permission explicite de l'utilisateur. Cela inclut : soumettre des reviews de PR, poster des commentaires, créer/fusionner des pull requests, pousser des commits, créer des branches ou des issues. Toujours rédiger le contenu localement et le présenter à l'utilisateur pour relecture AVANT toute publication.

## Quand l'utiliser

- Avant de committer, pour attraper les problèmes en amont
- Quand l'utilisateur demande de relire les changements, revoir le diff, etc.
- Invoqué via `/review-changes`

## Étapes

### 1. Déterminer le périmètre

Exécuter l'une des commandes suivantes selon l'intention :

```bash
# Modifications non stagées
git diff

# Modifications stagées
git diff --cached

# Toutes les modifications locales (stagées + non stagées) vs HEAD
git diff HEAD

# Modifications de la branche vs main
git diff main...HEAD
```

// turbo-all

Par défaut, utiliser `git diff HEAD` (toutes les modifications non committées).

Si le diff est volumineux (>500 lignes), commencer par `git diff HEAD --stat` pour un aperçu, puis passer fichier par fichier avec `git diff HEAD -- <chemin>`.

### 2. Passer en revue chaque fichier modifié

Pour chaque fichier modifié, évaluer selon **TOUS** les critères suivants :

#### Correction

- [ ] La logique fait-elle bien ce qu'elle prétend ?
- [ ] Les cas limites sont-ils gérés (`None`, listes vides, fichiers/dossiers manquants) ?
- [ ] Les chemins d'erreur sont-ils corrects (pas d'exceptions avalées, codes retour cohérents) ?
- [ ] Y a-t-il des problèmes de concurrence ou de thread-safety ?

#### Cohérence

- [ ] Le changement suit-il les patterns existants du projet ?
- [ ] Les conventions de nommage sont-elles respectées ? (Python : `snake_case` ; Vue/JS : `camelCase` pour les variables, `PascalCase` pour les composants)
- [ ] Le style est-il cohérent avec les fichiers environnants ?
- [ ] Les modèles SQLAlchemy suivent-ils le même pattern que ceux de `models.py` ? (`Mapped`, `mapped_column`, `_utcnow`)

#### Complétude

- [ ] Tous les fichiers nécessaires sont-ils modifiés (routes, modèles, schémas, composants Vue, docs) ?
- [ ] Reste-t-il des `TODO` / `FIXME` involontaires ?
- [ ] Le `README.md` a-t-il été mis à jour si nécessaire ?
- [ ] Les imports sont-ils propres (pas d'inutilisés, pas de manquants) ?
- [ ] Si un fichier a été renommé, toutes les références sont-elles à jour ?

#### Robustesse

- [ ] Les chemins fichiers sont-ils gérés avec `Path` et non par concaténation de chaînes ?
- [ ] Les ressources sont-elles correctement libérées (sessions DB, handles fichier) ?
- [ ] Les erreurs HTTP renvoient-elles les bons codes de statut et des messages explicites ?
- [ ] L'application gère-t-elle gracieusement les données manquantes ou malformées ?

#### Sécurité

- [ ] Y a-t-il des clés API ou des credentials codés en dur ?
- [ ] Les secrets sont-ils lus depuis l'environnement (`.env`), jamais loggés ni affichés ?
- [ ] Y a-t-il des risques de traversée de chemin (path traversal) dans les entrées utilisateur ?
- [ ] Les injections SQL sont-elles prévenues (utilisation de l'ORM, pas de requêtes brutes non paramétrées) ?
- [ ] Les mots de passe sont-ils hachés (bcrypt/argon2), jamais stockés en clair ?
- [ ] La protection CSRF est-elle en place pour les actions sensibles ?

#### Base de données & Modèles

- [ ] Les migrations/modifications de schéma sont-elles rétro-compatibles ?
- [ ] La contrainte `UNIQUE(user_id, segment_id)` est-elle préservée ?
- [ ] Les `CHECK` constraints (`label`, `niveau_breton`, `confidence`) sont-elles cohérentes ?
- [ ] Les relations (`relationship`, `ForeignKey`) sont-elles correctement définies ?
- [ ] Les sessions sont-elles correctement fermées (pas de fuite de connexion) ?

#### API (FastAPI)

- [ ] Les endpoints suivent-ils le pattern `/api/<ressource>` ?
- [ ] Les schémas Pydantic valident-ils correctement les entrées ?
- [ ] Les réponses d'erreur sont-elles explicites et structurées ?
- [ ] Le CORS est-il correctement configuré (dev vs prod) ?
- [ ] Les routes catch-all du SPA ne masquent-elles pas les routes API ?

#### Frontend (Vue 3 + Tailwind CSS)

- [ ] Les composants sont-ils réactifs et gèrent-ils correctement le cycle de vie (`onMounted`, `onUnmounted`) ?
- [ ] Les appels `fetch` / API gèrent-ils les erreurs (réseau, 4xx, 5xx) ?
- [ ] L'interface est-elle responsive (mobile + tablette) ?
- [ ] L'accessibilité est-elle respectée ? (taille police ≥ 16px, contraste AA, attributs `alt`)
- [ ] Les classes Tailwind sont-elles cohérentes avec le design system du projet ?

#### Intégrité des données d'annotation

- [ ] La séparation corpus brut / annotations est-elle maintenue (NF05) ?
- [ ] Chaque annotation est-elle bien horodatée et liée à un utilisateur (NF06) ?
- [ ] Le format d'export (JSONL/CSV) est-il conforme aux spécifications du PRD ?
- [ ] Les champs `label`, `confidence`, `corrected_text` respectent-ils les contraintes du schéma ?

### 3. Vérification croisée avec le contexte du projet

- Relire le `PRD.md` pour vérifier l'alignement avec les exigences
- Vérifier la cohérence avec le `README.md`
- S'assurer que les changements respectent les exigences non fonctionnelles (NF01–NF09)

### 4. Lint et vérification syntaxique

Uniquement s'il y a des changements de code :

#### Backend (Python)

```bash
source .venv/bin/activate && python -m py_compile backend/app/main.py 2>&1
```

```bash
for f in backend/app/*.py; do python -m py_compile "$f" 2>&1; done
```

#### Frontend (Vue / JS)

```bash
cd frontend && npx vue-tsc --noEmit 2>&1 || true
```

### 5. Smoke test

S'il y a des changements de code, lancer un test rapide :

#### Backend

```bash
source .venv/bin/activate && PYTHONPATH=. uvicorn backend.app.main:app --port 8000 &
sleep 2 && curl -s http://localhost:8000/api/hello && kill %1
```

#### Frontend

```bash
cd frontend && npm run build 2>&1
```

### 6. Produire le rapport de revue

Structurer le résultat comme suit :

```markdown
## Résumé de la revue

**Périmètre** : <ce qui a été revu, ex. « 3 fichiers, 47 insertions, 12 suppressions »>
**Verdict** : ✅ LGTM / ⚠️ Problèmes mineurs / ❌ Modifications demandées

## Problèmes trouvés

### 🔴 Critiques (à corriger impérativement)
- [fichier:ligne] Description du problème

### 🟡 Suggestions (à corriger de préférence)
- [fichier:ligne] Description de la suggestion

### 🔵 Détails (optionnel)
- [fichier:ligne] Description du détail

## Ce qui est bien fait
- Mention brève des points positifs

## Checklist
- [ ] Compile sans erreur (backend + frontend)
- [ ] Endpoints API fonctionnels
- [ ] Build frontend réussit
- [ ] Docs à jour (README.md)
- [ ] Schéma DB cohérent avec le PRD
- [ ] Contraintes d'intégrité préservées
```

### 7. Proposer de corriger les problèmes

Si des problèmes sont trouvés, demander à l'utilisateur :
> Souhaites-tu que je corrige les problèmes [critiques/suggérés] ?

NE PAS corriger automatiquement sans demander. Présenter les résultats d'abord, laisser l'utilisateur décider.

## Notes importantes

- Être **réellement critique** — le but est d'attraper les bugs avant qu'ils n'arrivent en production
- Ne pas approuver un diff avec un simple « LGTM » sauf s'il est véritablement propre
- Porter une attention particulière à : fuites de sessions DB, injections SQL, données d'annotation incohérentes, régression des contraintes d'intégrité, casse de l'interface responsive
- Si un changement semble incomplet (ex. : ajout d'un endpoint sans mise à jour du README), le signaler
- Toujours vérifier la conformité avec le `PRD.md` et les conventions du projet