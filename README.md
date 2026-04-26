# GTM Copilot

Ton copilote commercial qui pilote ta prospection LinkedIn et email en 30 min/jour, avec ton accord à chaque envoi. Il connaît ton business, parle ton ton, et ne fait jamais rien sans validation.

## Comment ça marche

Le copilote tourne en 4 couches :

1. **Tes outils** — choisis ton CRM (Airtable, Notion, NocoDB, ou custom) et ta passerelle email/LinkedIn (Unipile pour Outlook, Gmail, LinkedIn).
2. **Tes comptes** — connectés une fois via OAuth (LinkedIn, mail) et un token (CRM).
3. **Le repo** — cloné chez toi, contient le code Python (`plugins/`), les commandes (`.claude/skills/`), et ton contexte (`knowledge/`).
4. **Ton contexte** — qui tu es, ce que tu vends, à qui, ton ton, ta stratégie. Rempli via `/system init`.

## Quickstart

Trois lignes :

```bash
git clone https://github.com/studio-catapulte/gtm-copilot.git
cd gtm-copilot
cp .env.example .env
```

Ouvre Claude Code dans le dossier et tape :

```
/system init
```

La commande t'accompagne sur tout le reste : choix du CRM, creds Unipile, setup du venv Python, contexte business à partir de tes pointeurs (URL LinkedIn, site web, doc commerciale). Compte ~20-25 min selon ce que tu fournis.

Une fois fini, lance ta première routine en tapant : "Routine du matin".

## Pré-requis

- [Claude Code](https://claude.ai) installé (abonnement Claude Pro)
- Un compte [Unipile](https://www.unipile.com) (gratuit pour démarrer)
- Un CRM de ton choix (Airtable gratuit, Notion gratuit, NocoDB self-hosted, ou ta propre stack)

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
docs/               Guides setup et opérationnels
```

## Doc

- [`docs/SETUP.md`](docs/SETUP.md) — ce que fait `/system init` sous le capot, et référence des variables `.env`
- [`docs/crm/`](docs/crm/) — guides par CRM (Airtable, Notion, NocoDB, custom)
- [`docs/operators/`](docs/operators/) — guides opérateur (génération de hosted auth links Unipile, scopes Microsoft, etc.)

## Support

Issues : https://github.com/studio-catapulte/gtm-copilot/issues
