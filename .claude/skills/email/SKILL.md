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
stables) et **les adapters** (`adapters/`, un par outil). Le meme provider couvre
mail ET agenda (gog → Gmail+gCal, ms365 → Outlook+Cal, unipile → Outlook+Cal).

## Provider(s) actif(s)

Lire `CLAUDE.md > Outils actifs`, puis suivre l'adapter dans `adapters/<provider>.md`.

**Multi-compte assume** : une install peut avoir plusieurs boites (ex. deux comptes
Gmail via gog). CLAUDE.md liste alors les instances, ex :
`Email : gog [guillaume@studio-catapulte.com, guillaume@versohq.io]`. Les routines
iterent sur les instances declarees.

Adapters fournis : `gmail-gog` (CLI), `ms365-mcp` (serveur MCP), `unipile-outlook`
(legacy, script). En brancher un autre = 1 fichier `adapters/<x>.md`.

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

## Regles

- Un skill-process n'appelle JAMAIS un provider en dur : il passe par ce skill.
- **N'envoie / ne cree jamais sans validation** — montrer le draft, attendre l'accord.
- Si aucun provider email n'est declare dans CLAUDE.md → le signaler, proposer
  `/system init-repo`.
- Ajouter un provider = 1 fichier dans `adapters/` mappant les operations ci-dessus.
