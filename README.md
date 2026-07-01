# GTM Copilot

Ton copilote commercial qui pilote ta prospection LinkedIn et email en 30 min/jour, avec ton accord à chaque envoi. Il connaît ton business, parle ton ton, et ne fait jamais rien sans validation.

## Comment ça marche

Le copilote tourne en 4 couches :

1. **Tes outils (ports & adapters)** — les skills parlent en **capacités** (CRM, email, LinkedIn), et tu branches un **adapter** par capacité, une fois, dans `.env` :
   - **CRM** — Airtable, Notion, NocoDB fournis en exemples ; n'importe quel CRM (HubSpot, Attio, Folks, Pipedrive…) via un adapter custom (1 fichier). `CRM_PROVIDER=`
   - **Email + calendrier** — Gmail (CLI `gog`), Microsoft 365 (serveur MCP), ou Outlook via Unipile (legacy). `EMAIL_PROVIDER=`
   - **LinkedIn** — via Unipile (adapter unique).
2. **Tes comptes** — connectés une fois (OAuth / token / CLI selon l'adapter).
3. **Le repo** — cloné chez toi, contient les skills (`.claude/skills/`, avec le code Python des intégrations embarqué dans chaque skill) et ton contexte (`knowledge/`).
4. **Ton contexte** — qui tu es, ce que tu vends, à qui, ton ton, ta stratégie. Rempli via `/system init-repo`.

## Quickstart

Trois lignes :

```bash
git clone https://github.com/studio-catapulte/gtm-copilot.git
cd gtm-copilot
cp .env.example .env
```

Puis ouvre Claude Code **dans le dossier** (`claude` depuis `gtm-copilot/`, pas avant). Et invoque l'onboarding :

- **Mode explicite** : tape `/system init-repo`
- **Mode naturel** : dis simplement "premiere fois", "initialise le repo", ou "salut"

L'onboarding orchestre tout : choix des adapters (CRM, email, LinkedIn), setup adapté à chacun (CLI / MCP / venv Python), contexte business à partir de tes pointeurs (URL LinkedIn, site web, doc commerciale). Compte ~20-25 min selon ce que tu fournis.

Une fois fini, lance ta première routine en tapant : "Routine du matin".

> ⚠️ **Si Claude Code etait deja ouvert avant le clone**, redemarre-le dans le nouveau dossier. Les skills (`/system`, `/daily`, `/weekly`, etc.) ne sont detectees qu'au demarrage si le dossier `.claude/skills/` existait deja a ce moment.

## Pré-requis

- [Claude Code](https://claude.ai) installé (abonnement Claude Pro)
- Pour LinkedIn : un compte [Unipile](https://www.unipile.com) (gratuit pour démarrer)
- Pour l'email : au choix la CLI [`gog`](https://github.com/) (Gmail) ou [`@softeria/ms-365-mcp-server`](https://github.com/Softeria/ms-365-mcp-server) (Microsoft 365)
- Un CRM de ton choix (Airtable gratuit, Notion gratuit, NocoDB self-hosted, ou ta propre stack)

## Commandes

Chaque action s'invoque en double mode : phrase en français OU slash command. Choisis ce qui te va.

| Phrase | Slash | Ce qui se passe | Fréquence |
|---|---|---|---|
| "Routine du matin" | `/daily` | Check inbox + nouvelles connexions + relances + invitations LinkedIn | Quotidien |
| "Bilan de la semaine" | `/weekly` | Review : wins, pipeline, objectifs semaine prochaine | Hebdo |
| "Prepare mon RDV avec X" | `/prep-meeting X` | Profil LinkedIn + entreprise + questions suggérées | À la demande |
| "Trouve-moi des prospects" | `/sourcing` | Recherche LinkedIn + qualification + ajout CRM | À la demande |
| "Premiere fois" / "Initialise le repo" | `/system init-repo` | Setup technique + contexte business | 1x à l'install |
| "Fin de session" | `/system done` | Log de session + mise à jour des contextes | Fin de journée |

## Structure du repo

```
knowledge/          Ce que le copilote sait sur ton business
.claude/skills/     Ce que le copilote sait faire (skills = capacités)
   linkedin/          capacité LinkedIn (adapter : unipile, scripts embarqués)
   fathom/            capacité transcripts meetings (adapter : Fathom)
   daily/ weekly/ sourcing/ prep-meeting/ system/
   _shared/           ports & adapters transverses
      crm.md            port CRM     → providers/crm/{notion,airtable,nocodb,custom}.md
      email.md          port email   → providers/email/{gmail-gog,ms365-mcp,unipile-outlook}.md
docs/               Guides setup et opérationnels
```

**Port** = le contrat d'une capacité (opérations logiques, agnostique de l'outil).
**Adapter** = ce qui connecte un skill à un outil concret (CLI, script, ou serveur MCP).
Le binding capacité→adapter vit dans `.env` (`CRM_PROVIDER`, `EMAIL_PROVIDER`). Ajouter
un outil = écrire 1 fichier adapter, sans toucher aux skills.

## Doc

- [`docs/SETUP.md`](docs/SETUP.md) — ce que fait `/system init-repo` sous le capot, et référence des variables `.env`
- [`.claude/skills/_shared/providers/crm/`](.claude/skills/_shared/providers/crm/) — guides par CRM (Airtable, Notion, NocoDB, custom)
- [`.claude/skills/_shared/providers/email/`](.claude/skills/_shared/providers/email/) — adapters email (gog, ms365-mcp, unipile-outlook)

## Support

Issues : https://github.com/studio-catapulte/gtm-copilot/issues
