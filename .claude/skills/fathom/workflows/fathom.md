# Fathom — Transcripts et summaries de meetings

Wrapper REST autour de l'API Fathom (https://api.fathom.ai/external/v1/). Pas de
MCP officiel au 03-06-2026, on parle directement à l'API. Référence interne
appelée par le skill `/prep-meeting`.

## Pré-requis

- `FATHOM_API_KEY` dans `.env` à la racine du kit
- Venv Python : `.claude/skills/fathom/scripts/venv` (créé par `bash .claude/skills/fathom/scripts/setup.sh`)
- Compte Fathom (gratuit ou premium) avec accès API activé

## Lister les meetings

```python
import sys; sys.path.insert(0, '.claude/skills/fathom/scripts')
from fathom_client import FathomClient
client = FathomClient()

# Liste brute (10 derniers)
meetings = client.list_meetings(limit=10)

# Avec summaries inline
meetings = client.list_meetings(include_summary=True, limit=10)

# Avec transcripts inline (lourd, à éviter sauf besoin)
meetings = client.list_meetings(include_transcript=True, limit=5)
```

## Summary + transcript d'un meeting précis

```python
summary = client.get_summary(recording_id)
transcript = client.get_transcript(recording_id)
```

## Résoudre un identifiant ambigu

Le numéro qui apparaît dans une URL `https://fathom.video/calls/<id>` est un
**call_id**, PAS un recording_id. Le helper `resolve()` fait le mapping :

```python
# Depuis une URL collée
meta = client.resolve("https://fathom.video/calls/12345")

# Depuis un call_id seul
meta = client.resolve("12345")

# Depuis un recording_id déjà résolu (idempotent)
meta = client.resolve("abc-def-ghi")
```

## CLI rapide

```bash
source .claude/skills/fathom/scripts/venv/bin/activate

python .claude/skills/fathom/scripts/fathom_client.py meetings --limit 10 --with-summary
python .claude/skills/fathom/scripts/fathom_client.py summary RECORDING_ID
python .claude/skills/fathom/scripts/fathom_client.py transcript RECORDING_ID
python .claude/skills/fathom/scripts/fathom_client.py resolve https://fathom.video/calls/12345
```

## Pièges

- Le **call_id n'est pas un recording_id** — passer par `resolve()` ou
  `get_recording_by_call_id()` avant les appels summary/transcript.
- L'API renvoie 401 si la clé est révoquée ou si le plan Fathom n'a pas accès API.
- `include_transcript=True` sur `list_meetings` peut renvoyer plusieurs MB —
  réserver aux cas où on en a vraiment besoin.
