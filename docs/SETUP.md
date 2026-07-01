# Setup sous le capot

`/system init-repo` orchestre l'install. Cette page explique ce qu'il fait pour les users qui veulent comprendre avant de lancer, ou pour debug.

## Ce que fait `/system init-repo`

1. Vérifie/crée `.env` (depuis `.env.example`)
2. Te demande quel CRM choisir, te guide vers `.claude/skills/_shared/providers/crm/<type>.md`, écrit `CRM_PROVIDER` dans `.env`
3. Te demande tes credentials Unipile (DSN, API key, account_id par provider)
4. Lance `.claude/skills/linkedin/scripts/setup.sh` (crée le venv Python si absent)
5. Teste les connexions CRM + Unipile
6. Te demande tes pointeurs business (URL LinkedIn, site, doc commerciale)
7. Pré-remplit `CLAUDE.md` + `knowledge/` à partir des pointeurs
8. Te pose les questions ouvertes uniquement sur les trous restants

## Variables `.env` (référence)

### LinkedIn (adapter Unipile)

- `UNIPILE_DSN` — endpoint de ton tenant Unipile (avec `https://`)
- `UNIPILE_API_KEY` — clé API
- `UNIPILE_LINKEDIN_ACCOUNT_ID` — l'account_id LinkedIn

Tu trouves ces valeurs dans ton [Dashboard Unipile](https://dashboard.unipile.com).

### Email + Calendrier

`EMAIL_PROVIDER=<gmail-gog|ms365-mcp|unipile-outlook>` (port `_shared/email.md`) :

- `gmail-gog` — CLI `gog`, aucune var `.env` (gog gère son auth)
- `ms365-mcp` — serveur MCP `@softeria/ms-365-mcp-server`, auth via tool `login`
- `unipile-outlook` (legacy) — réutilise les creds Unipile ci-dessus + `UNIPILE_OUTLOOK_ACCOUNT_ID`

### CRM

`CRM_PROVIDER=<airtable|notion|nocodb|custom>` puis les variables correspondantes :

- Airtable : `AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`, `AIRTABLE_TABLE_ID`
- Notion : `NOTION_API_KEY`, `NOTION_DATABASE_ID`
- NocoDB : `NOCODB_URL`, `NOCODB_TOKEN`, `NOCODB_TABLE_ID`
- Custom : `CRM_CUSTOM_API_URL`, `CRM_CUSTOM_API_KEY` (voir `.claude/skills/_shared/providers/crm/custom.md`)

Voir [`.claude/skills/_shared/providers/crm/`](crm/) pour les guides détaillés par CRM.
