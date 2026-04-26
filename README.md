# GTM Copilot

Ton copilote commercial qui pilote ta prospection LinkedIn et email en 30 min/jour, avec ton accord à chaque envoi. Il connaît ton business, parle ton ton, et ne fait jamais rien sans validation.

## Comment ça marche

Le copilote tourne en 4 couches :

1. **Tes outils** — choisis ton CRM (Airtable, Notion, NocoDB, ou custom) et ta passerelle email/LinkedIn (Unipile pour Outlook, Gmail, LinkedIn).
2. **Tes comptes** — connectés une fois via OAuth (LinkedIn, mail) et un token (CRM).
3. **Le repo** — cloné chez toi, contient le code Python (`plugins/`), les commandes (`.claude/skills/`), et ton contexte (`knowledge/`).
4. **Ton contexte** — qui tu es, ce que tu vends, à qui, ton ton, ta stratégie. Rempli une fois via `/system init`.

## Quickstart

Voir le guide détaillé : [`docs/SETUP.md`](docs/SETUP.md). En résumé :

1. `git clone studio-catapulte/gtm-copilot && cd gtm-copilot`
2. `cp .env.example .env`, choisis ton CRM, et remplis les variables (voir [`docs/crm/`](docs/crm/))
3. `cd plugins/unipile && ./setup.sh`
4. Récupère tes credentials Unipile auprès de Nefia (DSN, API key, account_id) et colle-les dans `.env`
5. Ouvre Claude Code dans le dossier et tape `/system init` (~15-20 min selon les pointeurs fournis)
6. Lance ta première routine : "Routine du matin"

## Commandes

| Dis ça | Ce qui se passe | Fréquence |
|---|---|---|
| "Routine du matin" | Check inbox + nouvelles connexions + relances + invitations LinkedIn | Quotidien |
| "Weekly" | Review : wins, pipeline, objectifs semaine prochaine | Hebdo |
| "Prepare mon RDV avec X" | Profil LinkedIn + entreprise + questions suggérées | À la demande |
| "Trouve-moi des prospects" | Recherche LinkedIn + qualification + ajout CRM | À la demande |
| "Fais des slides pour X" | Présentation HTML personnalisée pour un prospect | À la demande |

## Structure du repo

```
knowledge/          Ce que le copilote sait sur ton business
.claude/skills/     Ce que le copilote sait faire
tools/              Schémas et docs internes
plugins/            Code Python pour les appels API (Unipile)
docs/               Guides setup (fondateur + opérateur)
```

## Doc

- [`docs/SETUP.md`](docs/SETUP.md) — guide d'install fondateur (~15 min)
- [`docs/crm/`](docs/crm/) — guides par CRM (Airtable, Notion, NocoDB, custom)
- [`docs/operators/`](docs/operators/) — guides côté Nefia (opérateur)

## Support

Nefia — contact@nefia.fr
