# GTM Copilot

Ton copilote commercial qui pilote ta prospection LinkedIn et email en 30 min/jour, avec ton accord à chaque envoi. Il connaît ton business, parle ton ton, et ne fait jamais rien sans validation.

## Comment ça marche

Le copilote tourne en 4 couches :

1. **Tes outils (skills-outils)** — les routines parlent en **capacités** (CRM, email, LinkedIn, meeting-notes) ; chaque capacité est un **skill-outil** dont le `SKILL.md` contient le contrat + le mapping de l'outil actif. Tu branches un outil par capacité, une fois, en le déclarant dans `CLAUDE.md > Outils actifs` :
   - **CRM** — Airtable, Notion, NocoDB fournis en exemples ; n'importe quel CRM (HubSpot, Attio, Folks, Pipedrive…) via un adapter custom (1 fichier).
   - **Email + calendrier** — Gmail (CLI `gog`), Microsoft 365 (serveur MCP), ou Outlook via Unipile (legacy).
   - **LinkedIn** — via Unipile. **Meeting-notes** — via Fathom.
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
.claude/skills/     Ce que le copilote sait faire
   # routines (parlent capacités)
   daily/ weekly/ sourcing/ prep-meeting/ system/
   # skills-outils (contrat + mapping de l'outil actif inline)
   crm/           SKILL.md (contrat CRM + mapping de l'outil actif)
   email/         SKILL.md (contrat email + mapping de l'outil actif)
   linkedin/      capacité LinkedIn (Unipile, scripts embarqués)
   meeting-notes/ SKILL.md + scripts/ (Fathom)
docs/               Setup par outil (crm/, email/) + guides
```

**Skill-outil** = une capacité (CRM, email…) ; son `SKILL.md` porte le **contrat**
(opérations + schéma, agnostique) **et le mapping de l'outil actif, inline**. Les guides
de setup des autres outils vivent dans `docs/{crm,email}/`. **Quel outil est branché**
se déclare dans `CLAUDE.md > Outils actifs` ; **les clés** vivent dans `.env`. Changer
d'outil = adapter la section « Adapter actif » du skill, sans toucher aux routines.

## Doc

- [`docs/SETUP.md`](docs/SETUP.md) — ce que fait `/system init-repo` sous le capot, et référence des variables `.env`
- [`docs/crm/`](docs/crm/) — guides de setup par CRM (Airtable, Notion, NocoDB, custom)
- [`docs/email/`](docs/email/) — setup email (gog, ms365-mcp, unipile-outlook)

## Support

Issues : https://github.com/studio-catapulte/gtm-copilot/issues
