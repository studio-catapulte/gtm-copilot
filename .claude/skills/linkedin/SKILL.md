---
name: linkedin
description: |
  Capacite LinkedIn (Pack Pro) : recherche/profils LinkedIn et messagerie
  (LinkedIn/WhatsApp/IG). Adapter unique : Unipile (scripts Python embarques).
  A utiliser quand un autre skill (sourcing, daily, prep-meeting) a besoin
  d'agir sur LinkedIn/messagerie, ou pour (re)configurer l'acces.

  Triggers: /linkedin, "connecte linkedin", "cherche sur linkedin",
  "envoie un message linkedin", "setup linkedin".

  Config : credentials lus depuis .env (a la racine du repo). Aucune cle en dur.
---

# /linkedin — Capacite LinkedIn (adapter : Unipile)

Skill nomme par la **capacite** (LinkedIn). Derriere, un **adapter unique = Unipile**
colle au skill : code Python (`scripts/`), cookbooks (`workflows/`), setup venv.

> Le jour ou un 2e provider LinkedIn existe, on extraira un port `_shared/`. Pas avant.
> L'email/calendrier ne passe PAS par ici — voir le port `_shared/email.md`.

## Routing

| Besoin | Workflow |
|--------|----------|
| Recherche / profils LinkedIn | → Lire `workflows/linkedin.md` |
| Messagerie (LinkedIn / WhatsApp / IG) | → Lire `workflows/messaging.md` |
| Enrichissement de contacts (FullEnrich) | → Lire `workflows/enrichment.md` |

## Setup (premiere utilisation)

```bash
cd .claude/skills/linkedin/scripts && ./setup.sh
```

`setup.sh` calcule son chemin via `BASH_SOURCE` (independant du cwd) et cree
`venv/` a cote de lui-meme (idempotent). Aussi appele par `/system init-repo`.

## Invocation des scripts

Deux styles, tous deux depuis la racine du repo :

- **CLI via venv** :
  ```bash
  cd .claude/skills/linkedin/scripts && source venv/bin/activate
  python linkedin_client.py search-people --keywords "..." --location "..."
  ```
- **Import in-process** :
  ```python
  import sys; sys.path.insert(0, '.claude/skills/linkedin/scripts')
  from linkedin_client import UnipileLinkedInClient
  client = UnipileLinkedInClient()
  ```

## Config

`scripts/unipile_auth.py` charge le `.env` en remontant jusqu'a 6 dossiers parents
(`_load_env_files()`), sans jamais ecraser une variable deja exportee. Cles requises
dans `.env` : `UNIPILE_API_KEY`, `UNIPILE_DSN`, et selon usage
`UNIPILE_LINKEDIN_ACCOUNT_ID`. Voir `docs/SETUP.md`.

## Regles

- Aucune cle en dur : tout via `.env`.
- Socle appele par d'autres skills ; rarement invoque seul sauf setup/besoin ponctuel.
