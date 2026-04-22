# CRM — Source de verite du pipeline

Le CRM est la pierre angulaire du copilote. Tous les skills lisent et ecrivent dedans.
Ce fichier explique comment le copilote interagit avec le CRM du fondateur.

## Quel CRM ?

Le type de CRM est defini dans `.env` sous `CRM_TYPE`. 4 modes possibles :

| Mode | Quand | Config .env |
|------|-------|-------------|
| **airtable** (defaut) | Nouveau client, gratuit, API simple | `AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`, `AIRTABLE_TABLE_ID` |
| **notion** | Client qui utilise deja Notion | `NOTION_API_KEY`, `CRM_DATABASE_ID` |
| **nocodb** | Client tech, self-hosted, pas de lock-in | `NOCODB_URL`, `NOCODB_API_KEY`, `NOCODB_BASE_ID`, `NOCODB_TABLE_ID` |
| **custom** | Client avec HubSpot, Pipedrive, etc. | `CRM_CUSTOM_API_URL`, `CRM_CUSTOM_API_KEY` |

## Schema de champs (commun a tous les modes)

| Champ | Type | Usage |
|-------|------|-------|
| Nom | Texte | Nom complet du contact |
| Entreprise | Texte | Nom de l'entreprise |
| Statut | Select | Etape du pipeline (voir CLAUDE.md) |
| Dernier contact | Date | Date du dernier echange |
| Next | Date | Date de la prochaine action a faire |
| Notes | Texte long | Contexte, historique des echanges |
| LinkedIn | URL | Profil LinkedIn |
| Email | Email | Email pro |
| Telephone | Texte | Telephone |
| Source | Select | Comment on l'a trouve (LinkedIn, Salon, Referral...) |

## Setup Airtable (mode par defaut)

### 1. Creer un compte Airtable

Aller sur airtable.com, creer un compte gratuit.

### 2. Creer la base

1. Creer une nouvelle base "CRM [Nom Entreprise]"
2. Renommer la premiere table en "Contacts"
3. Creer les champs selon le schema ci-dessus :
   - Nom → Single line text (deja present, renommer)
   - Entreprise → Single line text
   - Statut → Single select → ajouter les etapes du pipeline (voir CLAUDE.md)
   - Dernier contact → Date
   - Next → Date
   - Notes → Long text
   - LinkedIn → URL
   - Email → Email
   - Telephone → Phone number
   - Source → Single select (LinkedIn, Salon, Referral, Cold Call, Inbound)

### 3. Generer un API token

1. Aller sur airtable.com/create/tokens
2. Creer un token avec les permissions :
   - `data.records:read`
   - `data.records:write`
   - `schema.bases:read`
3. Scope : la base creee
4. Copier le token

### 4. Configurer le .env

```bash
CRM_TYPE=airtable
AIRTABLE_API_KEY=pat_xxxxx
AIRTABLE_BASE_ID=appXXXXXXXXXX    # visible dans l'URL de la base
AIRTABLE_TABLE_ID=tblXXXXXXXXXX   # visible dans l'URL de la table
```

### 5. Configurer le MCP (si Airtable MCP disponible)

Ajouter dans `.mcp.json` :

```json
{
  "mcpServers": {
    "airtable": {
      "command": "npx",
      "args": ["-y", "@airtable/mcp-server"],
      "env": {
        "AIRTABLE_API_KEY": "pat_xxxxx"
      }
    }
  }
}
```

**Important** : ajouter `.mcp.json` au `.gitignore` (contient des cles API).

### 6. Importer les contacts existants

Si le fondateur a une liste de contacts (Google Sheet, Excel, CSV) :
1. Exporter en CSV
2. Importer dans Airtable via l'interface (Add records -> Import)
3. Mapper les colonnes vers les champs du schema

## Setup Notion

Voir la documentation Notion MCP. Creer une database avec les champs du schema,
configurer `NOTION_API_KEY` et `CRM_DATABASE_ID` dans `.env`.

## Setup NocoDB

Deployer NocoDB (Docker), creer la table avec le schema, configurer les variables dans `.env`.

## Operations CRM (pour les skills)

Les skills utilisent ces operations logiques :

| Operation | Usage |
|-----------|-------|
| **Lister par statut** | Pipeline snapshot (briefing, bilan) |
| **Filtrer Next <= aujourd'hui** | Follow-ups dus (relances, briefing) |
| **Chercher par nom/email** | Matcher un prospect (inbox, enrichment) |
| **Creer un contact** | Nouveau lead (prospection) |
| **Mettre a jour** | Apres chaque action (tous les skills) |
| **Compter par statut** | KPIs (bilan) |

## Regles

1. **CRM = source de verite.** Ne jamais deviner, toujours lire le CRM.
2. **Toujours verifier les doublons** avant de creer un contact (chercher par LinkedIn URL ou email).
3. **Toujours inclure le profil LinkedIn** quand disponible.
4. **Mettre a jour apres chaque action** : Dernier contact, Next, Notes.
