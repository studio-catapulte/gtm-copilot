# Port — Email + Calendrier

Contrat **capacite email/calendrier**, agnostique du provider. Les skills
(`daily`, `prep-meeting`…) appellent ces operations logiques ; ils ne connaissent
jamais l'outil concret. Le choix du provider se fait **une fois** dans `.env`.

## Binding

```
EMAIL_PROVIDER=gmail-gog     # ou ms365-mcp, ou unipile-outlook (legacy)
```

Lire `EMAIL_PROVIDER`, puis suivre l'adapter correspondant :

| EMAIL_PROVIDER | Adapter | Nature |
|----------------|---------|--------|
| `gmail-gog` | `providers/email/gmail-gog.md` | CLI (`gog`) |
| `ms365-mcp` | `providers/email/ms365-mcp.md` | serveur MCP |
| `unipile-outlook` | `providers/email/unipile-outlook.md` | script Python (legacy) |

Le meme provider couvre **mail ET calendrier** (gog fait Gmail+gCal, ms365 fait
Outlook+Cal, unipile fait Outlook+Cal). Pas de binding calendrier separe.

## Operations logiques (le contrat)

Chaque adapter doit fournir un mapping concret pour :

**Mail**
- `list-inbox(unread_only?, limit)` — lister l'inbox
- `search(query, limit)` — rechercher des messages
- `get(message_id)` — lire un message complet
- `send(to, subject, body, cc?)` — envoyer un mail
- `archive(message_id)` / `mark-read(message_id)` — organiser

**Calendrier**
- `list-events(from, to)` — evenements sur une periode
- `search-events(query)` — chercher un evenement
- `create-event(title, from, to, attendees?)` — creer un evenement

## Regles

- Un skill n'appelle JAMAIS un provider en dur : il passe par ce port.
- Si `EMAIL_PROVIDER` est absent → le signaler et proposer `/system init-repo`.
- Ajouter un provider email = ecrire 1 fichier dans `providers/email/` qui mappe
  les operations ci-dessus, et l'ajouter au tableau de binding.
