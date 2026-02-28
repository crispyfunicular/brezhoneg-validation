---
description: Créer un commit propre avec un message conventionnel après validation de la revue
---

# Créer un commit

Workflow pour produire un commit propre et bien documenté. S'assure que la revue a eu lieu et que l'utilisateur valide chaque étape.

RÈGLE CRITIQUE : NE JAMAIS exécuter `git commit`, `git push`, ou toute action d'écriture git sans l'accord explicite de l'utilisateur. Toujours présenter le message de commit pour relecture AVANT de l'exécuter.

## Quand l'utiliser

- Après avoir terminé une modification et validé la revue
- Quand l'utilisateur demande de committer, commit, save, etc.
- Invoqué via `/commit`

## Étapes

### 1. Vérifier que la revue a été effectuée

Commencer par vérifier si une revue a été faite dans cette session de conversation.

Si la revue **n'a PAS** été faite, suggérer à l'utilisateur :
> Les modifications n'ont pas encore été revues. Souhaites-tu lancer `/review-changes` avant de committer ?

Attendre la réponse de l'utilisateur avant de continuer. Ne **jamais** committer sans cet échange.

### 2. Examiner les modifications à committer

// turbo-all

```bash
git status
```

```bash
git diff HEAD --stat
```

Si nécessaire, examiner le diff détaillé pour rédiger un message pertinent :

```bash
git diff HEAD
```

### 3. Proposer le staging

Présenter à l'utilisateur la liste des fichiers modifiés et proposer le staging :

- Si tous les fichiers vont ensemble → proposer `git add -A`
- Si certains fichiers devraient être dans des commits séparés → le signaler et proposer un découpage logique

**Attendre la validation de l'utilisateur** avant d'exécuter le `git add`.

### 4. Rédiger le message de commit

Utiliser le format **Conventional Commits** en français :

```
<type>(<portée>): <description courte>

<corps optionnel — détails, contexte, justification>
```

#### Types autorisés

| Type | Usage |
|------|-------|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `refactor` | Refactorisation sans changement fonctionnel |
| `style` | Formatage, CSS, sans changement logique |
| `docs` | Documentation uniquement |
| `test` | Ajout ou modification de tests |
| `chore` | Maintenance, dépendances, config, CI |
| `perf` | Amélioration de performance |

#### Portées courantes pour ce projet

| Portée | Fichiers concernés |
|--------|-------------------|
| `api` | `backend/app/routes/`, `backend/app/main.py` |
| `models` | `backend/app/models.py`, `backend/app/database.py` |
| `ui` | `frontend/src/` |
| `db` | Schéma, migrations, scripts d'import |
| `auth` | Authentification, sessions |
| `export` | Scripts d'export annotations |
| `config` | `.gitignore`, `requirements.txt`, `package.json`, Docker |
| `docs` | `README.md`, `PRD.md` |

#### Règles pour le message

- **Description courte** : impératif présent, minuscule, pas de point final, ≤ 72 caractères
- **Corps** : expliquer le *pourquoi*, pas le *quoi* (le diff montre déjà le quoi)
- **Langue** : français pour la description, anglais acceptable pour les termes techniques

#### Exemples

```
feat(api): ajouter l'endpoint d'export des annotations en JSONL

Permet aux chercheurs de télécharger les annotations filtrées par
corpus source et par label. Format conforme au PRD annexe B.
```

```
fix(models): corriger la contrainte CHECK sur niveau_breton

Le niveau "confirmé" utilisait un accent qui n'était pas cohérent
avec la valeur stockée ("confirme" sans accent).
```

```
chore(config): ajouter Pillow aux dépendances backend
```

### 5. Présenter le message à l'utilisateur

Afficher le message de commit proposé et demander validation :

> Voici le message de commit proposé :
>
> ```
> <message>
> ```
>
> ✅ C'est bon ? Je committe ?

**Attendre la validation explicite** avant d'exécuter quoi que ce soit.

### 6. Exécuter le commit

Seulement après accord de l'utilisateur :

```bash
git add -A  # ou les fichiers spécifiques validés à l'étape 3
```

```bash
git commit -m "<message validé>"
```

Si le commit a un corps multi-ligne, utiliser un fichier temporaire :

```bash
cat > /tmp/commit_msg.txt << 'EOF'
<message complet>
EOF
git commit -F /tmp/commit_msg.txt
rm /tmp/commit_msg.txt
```

### 7. Confirmer le résultat

```bash
git log -1 --stat
```

Présenter le résultat à l'utilisateur.

**Ne PAS proposer de `git push`** sauf si l'utilisateur le demande explicitement.

## Notes importantes

- **Chaque étape nécessitant une action git requiert l'accord de l'utilisateur**
- Privilégier des commits atomiques : un commit = un changement logique cohérent
- Si les modifications touchent des aspects très différents (ex. backend + docs + config), proposer de découper en plusieurs commits
- Ne jamais inclure de fichiers générés (`node_modules/`, `dist/`, `*.db`, `__pycache__/`) — vérifier le `.gitignore`
- En cas de doute sur le type ou la portée, demander à l'utilisateur
