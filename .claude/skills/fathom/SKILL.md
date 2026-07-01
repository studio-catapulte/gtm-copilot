---
name: fathom
description: |
  Integration Fathom (Pack Pro) : transcripts, summaries et action items de
  meetings enregistres, via l'API REST Fathom (pas de MCP officiel).
  Skill autoportant : script Python + workflow d'invocation + setup venv.
  A utiliser quand un skill (prep-meeting, done) a besoin de ce qui a ete dit
  dans un call passe, ou pour recuperer le transcript/summary d'un meeting.

  Triggers: /fathom, "recupere le transcript", "resume ce call", "action items du RDV",
  "qu'est-ce qui s'est dit avec X", "setup fathom".

  Config : FATHOM_API_KEY dans .env (racine du repo). Aucune cle en dur.
---

# /fathom — Transcripts et summaries de meetings

Skill autoportant hebergeant l'integration Fathom : le code Python (`scripts/`),
le cookbook d'invocation (`workflows/`), et le setup du venv.

## Routing

| Besoin | Workflow |
|--------|----------|
| Lister / resoudre / resumer / transcrire un meeting | → Lire `workflows/fathom.md` |

## Setup (premiere utilisation)

```bash
cd .claude/skills/fathom/scripts && ./setup.sh
```

`setup.sh` calcule son chemin via `BASH_SOURCE` et cree `venv/` a cote de lui-meme
(idempotent). Aussi appele par `/system init-repo`.

## Invocation

Deux styles, depuis la racine du repo :

- **CLI via venv** :
  ```bash
  cd .claude/skills/fathom/scripts && source venv/bin/activate
  python fathom_client.py meetings --limit 10
  python fathom_client.py resolve <call_id_ou_url>   # → recording_id
  python fathom_client.py transcript <recording_id>
  ```
- **Import in-process** :
  ```python
  import sys; sys.path.insert(0, '.claude/skills/fathom/scripts')
  from fathom_client import FathomClient
  client = FathomClient()
  ```

## Config

`scripts/fathom_client.py` charge le `.env` a la racine (via `find_kit_root()` qui
remonte vers le `CLAUDE.md`, puis `_load_dotenv()` sans ecraser l'existant).
Cle requise : `FATHOM_API_KEY`. Un `call_id` (numero d'URL `/calls/<id>`) n'est PAS
un `recording_id` : le resoudre via `resolve` avant summary/transcript.

## Regles

- Aucune cle en dur : tout via `.env`.
- Socle appele par d'autres skills (prep-meeting, done) ; rarement invoque seul.
