---
name: email
description: |
  Capacite email + calendrier. Skill-tool appele par les skills-process (daily,
  prep-meeting) pour lire l'inbox, envoyer des mails, gerer l'agenda. L'outil concret
  (Gmail via gog, Microsoft 365 via MCP, Outlook via Unipile) est declare dans
  CLAUDE.md > Outils actifs.

  Triggers: /email, "mes mails", "checke l'inbox", "envoie un mail", "mon agenda".

  Ce skill n'est en general PAS invoque seul : socle reference par les routines.
  Aucune cle en dur : credentials dans .env (pour les adapters qui en ont).
---

# /email — Capacite email + calendrier

Skill-tool encapsulant l'email et le calendrier. Contient **le contrat** (operations
stables) et le **mapping de l'outil actif** (inline plus bas). Le meme provider couvre
mail ET agenda (gog → Gmail+gCal, ms365 → Outlook+Cal, unipile → Outlook+Cal).

## Outil(s) actif(s)

Declare dans `CLAUDE.md > Outils actifs`. Le mapping de l'outil actif est **inline plus
bas**. Autres outils (setup) : `docs/email/` (`gmail-gog.md`, `ms365-mcp.md`,
`unipile-outlook/`).

**Multi-compte assume** : une install peut avoir plusieurs boites. CLAUDE.md liste les
instances, ex : `Email : gog [guillaume@studio-catapulte.com, guillaume@versohq.io]`.
Les routines iterent sur les instances declarees.

---

## Contrat (operations logiques)

Chaque adapter mappe ces operations sur son mecanisme concret.

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

---

## Adapter actif — gog (Gmail + Calendar)

> Defaut fourni. CLI `gog`, compte via `-a <email>`, `-j` pour du JSON. Aucune cle
> `.env` (gog gere son auth). Setup : `docs/email/gmail-gog.md`.

Mail (syntaxe de recherche Gmail) :

| Operation | Commande |
|-----------|----------|
| `list-inbox(unread)` | `gog -a <acct> gmail search "in:inbox is:unread" -j --limit 50` |
| `search(query)` | `gog -a <acct> gmail search "<query Gmail>" -j` |
| `get(id)` | `gog -a <acct> gmail get <messageId>` |
| `send(...)` | `gog -a <acct> gmail send --to <x> --subject "<s>" --body "<b>"` |
| `archive(id)` / `mark-read(id)` | `gog -a <acct> gmail archive <id>` / `... mark-read <id>` |

Calendrier :

| Operation | Commande |
|-----------|----------|
| `list-events(from,to)` | `gog -a <acct> calendar events -j --from <ISO> --to <ISO>` |
| `search-events(q)` | `gog -a <acct> calendar search "<q>" -j` |
| `create-event(...)` | `gog -a <acct> calendar create <calendarId> --title "<t>" --from <ISO> --to <ISO>` |

`gog <cmd> --help` pour les flags exacts. Pour les autres outils (ms365 MCP,
unipile-outlook legacy), voir `docs/email/`.

## Regles

- Un skill-process n'appelle JAMAIS un provider en dur : il passe par ce skill.
- **N'envoie / ne cree jamais sans validation** — montrer le draft, attendre l'accord.
- Si aucun provider email n'est declare dans CLAUDE.md → le signaler, proposer
  `/system init-repo`.
- Ajouter/changer de provider = adapter la section « Adapter actif » ci-dessus
  (setup des autres outils : `docs/email/`).
