---
name: meeting-notes
description: |
  Capacite meeting-notes : transcripts, summaries et action items de reunions
  enregistrees. Skill-tool appele par prep-meeting / done pour repartir de ce qui
  s'est dit dans un call. L'outil concret (Fathom, et potentiellement Fireflies,
  tl;dv…) est declare dans CLAUDE.md > Outils actifs.

  Triggers: /meeting-notes, "recupere le transcript", "resume ce call",
  "action items du RDV", "qu'est-ce qui s'est dit avec X".

  Ce skill n'est en general PAS invoque seul : socle reference par les routines.
  Credentials dans .env (pour les adapters qui en ont).
---

# /meeting-notes — Transcripts & summaries de reunions

Skill-tool encapsulant l'acces aux notes de reunion. Contrat en **lecture seule**,
minuscule et vraiment agnostique — d'ou l'interet d'un adapter.

## Provider actif

Lire `CLAUDE.md > Outils actifs`. L'adapter actif (Fathom) est inline plus bas ; sa config detaillee est dans `fathom-reference.md`.

Outil fourni : **Fathom** (API REST, headless-safe ; mapping inline + `scripts/`).
D'autres outils du marche (Fireflies = MCP, tl;dv = REST, Granola = local-first sans
API headless fiable) peuvent etre branches en remplacant la section « Adapter actif »
— non fournis pour ne pas promettre ce qu'on ne maintient pas.

---

## Contrat (operations, lecture seule)

| Operation | Usage |
|---|---|
| `resolve(url \| call_id)` | Resoudre un identifiant vers l'id interne du meeting |
| `transcript(id)` | Transcript segmente |
| `summary(id)` | Resume structure |
| `action-items(id)` | Taches / next steps issus du call |
| `list(limit)` | Derniers meetings |

---

## Adapter actif : Fathom

Setup (venv, idempotent — aussi appele par `/system init-repo`) :

```bash
cd .claude/skills/meeting-notes/scripts && ./setup.sh
```

Invocation :

```bash
cd .claude/skills/meeting-notes/scripts && source venv/bin/activate
python fathom_client.py meetings --limit 10
python fathom_client.py resolve <call_id_ou_url>   # → recording_id
python fathom_client.py transcript <recording_id>
```

Détails d'invocation + notes API : `fathom-reference.md`. Cle requise :
`FATHOM_API_KEY` dans `.env`. Un `call_id` (numero d'URL `/calls/<id>`) n'est PAS un
`recording_id` : le resoudre via `resolve` d'abord.

## Regles

- Aucune cle en dur : tout via `.env`.
- Socle appele par d'autres skills (prep-meeting, done) ; rarement invoque seul.
