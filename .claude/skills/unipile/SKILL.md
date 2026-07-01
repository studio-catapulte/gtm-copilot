---
name: unipile
description: |
  Integration Unipile (Pack Pro) : LinkedIn, messagerie (LinkedIn/WhatsApp/IG),
  et Outlook (email + calendrier) via un compte Unipile connecte.
  Skill autoportant : scripts Python + workflows d'invocation + setup venv.
  A utiliser quand un autre skill (sourcing, daily, prep-meeting) a besoin
  d'agir sur LinkedIn/messagerie/Outlook, ou pour (re)configurer l'acces Unipile.

  Triggers: /unipile, "configure unipile", "connecte linkedin", "envoie un message linkedin",
  "cherche sur linkedin", "mes emails outlook", "setup unipile".

  Config : credentials lus depuis .env (a la racine du repo). Aucune cle en dur.
---

# /unipile — Integration Unipile (Pack Pro)

Skill autoportant hebergeant l'integration Unipile : le code Python (`scripts/`),
les cookbooks d'invocation (`workflows/`), et le setup du venv.

## Routing

| Besoin | Workflow |
|--------|----------|
| Recherche / profils LinkedIn | → Lire `workflows/linkedin.md` |
| Messagerie (LinkedIn / WhatsApp / IG) | → Lire `workflows/messaging.md` |
| Outlook (email + calendrier) | → Lire `workflows/outlook.md` |
| Enrichissement de contacts (FullEnrich) | → Lire `workflows/enrichment.md` |

## Setup (premiere utilisation)

Le venv et les dependances s'installent via le setup embarque :

```bash
cd .claude/skills/unipile/scripts && ./setup.sh
```

`setup.sh` calcule son chemin via `BASH_SOURCE` (independant du cwd) et cree
`venv/` a cote de lui-meme (idempotent). Ce setup est aussi appele par
`/system init-repo`.

## Invocation des scripts

Deux styles, tous deux depuis la racine du repo :

- **CLI via venv** :
  ```bash
  cd .claude/skills/unipile/scripts && source venv/bin/activate
  python linkedin_client.py search-people --keywords "..." --location "..."
  ```
- **Import in-process** :
  ```python
  import sys; sys.path.insert(0, '.claude/skills/unipile/scripts')
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
- Ce skill est un socle appele par d'autres skills ; il n'est generalement pas
  invoque seul sauf pour le setup ou un besoin ponctuel.
