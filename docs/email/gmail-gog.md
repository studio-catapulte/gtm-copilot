# Adapter email — gmail-gog

Mappe le port `../../.claude/skills/email/SKILL.md` sur la CLI **`gog`** (Google : Gmail + Calendar).
Provider par defaut pour un ecosysteme Google.

## Pre-requis

- CLI `gog` installee et un compte Google connecte (OAuth).
- Le compte cible passe via `-a <email>` (ex : `gog -a prospection@boite.com`).
- `-j` pour une sortie JSON scriptable.

## Mapping des operations

**Mail** (`gog gmail …`, syntaxe de recherche Gmail)

| Operation | Commande |
|-----------|----------|
| `list-inbox(unread)` | `gog -a <acct> gmail search "in:inbox is:unread" -j --limit 50` |
| `search(query)` | `gog -a <acct> gmail search "<query Gmail>" -j` |
| `get(id)` | `gog -a <acct> gmail get <messageId>` |
| `send(...)` | `gog -a <acct> gmail send --to <x> --subject "<s>" --body "<b>"` |
| `archive(id)` | `gog -a <acct> gmail archive <messageId>` |
| `mark-read(id)` | `gog -a <acct> gmail mark-read <messageId>` |

**Calendrier** (`gog calendar …`)

| Operation | Commande |
|-----------|----------|
| `list-events(from,to)` | `gog -a <acct> calendar events -j --from <ISO> --to <ISO>` |
| `search-events(query)` | `gog -a <acct> calendar search "<query>" -j` |
| `create-event(...)` | `gog -a <acct> calendar create <calendarId> --title "<t>" --from <ISO> --to <ISO>` |

## Notes

- `gog <cmd> --help` pour les flags exacts (l'outil bouge : verifier avant d'affirmer).
- Rien a installer cote repo (pas de venv) : `gog` est une CLI systeme.
