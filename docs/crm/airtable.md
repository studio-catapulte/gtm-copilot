# Setup CRM Airtable

Guide pas à pas pour configurer Airtable comme source de vérité du pipeline du copilote (mode CRM par défaut, gratuit, API simple).

## 1. Créer un compte Airtable

Aller sur [airtable.com](https://airtable.com), créer un compte gratuit.

## 2. Créer la base

1. Créer une nouvelle base "CRM [Nom Entreprise]"
2. Renommer la première table en "Contacts"
3. Créer les champs selon le schéma commun (voir [`../../tools/crm.md`](../../tools/crm.md)) :
   - Nom → Single line text (déjà présent, renommer)
   - Entreprise → Single line text
   - Statut → Single select → ajouter les étapes du pipeline (voir `CLAUDE.md`)
   - Dernier contact → Date
   - Next → Date
   - Notes → Long text
   - LinkedIn → URL
   - Email → Email
   - Téléphone → Phone number
   - Source → Single select (LinkedIn, Salon, Referral, Cold Call, Inbound)

## 3. Générer un API token

1. Aller sur [airtable.com/create/tokens](https://airtable.com/create/tokens)
2. Créer un token avec les permissions :
   - `data.records:read`
   - `data.records:write`
   - `schema.bases:read`
3. Scope : la base créée
4. Copier le token (commence par `pat_...`)

## 4. Configurer le `.env`

```bash
CRM_TYPE=airtable
AIRTABLE_API_KEY=pat_xxxxx
AIRTABLE_BASE_ID=appXXXXXXXXXX    # visible dans l'URL de la base
AIRTABLE_TABLE_ID=tblXXXXXXXXXX   # visible dans l'URL de la table
```

## 5. Configurer le MCP (si Airtable MCP disponible)

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

**Important** : ajouter `.mcp.json` au `.gitignore` (contient des clés API).

## 6. Importer les contacts existants

Si tu as une liste de contacts (Google Sheet, Excel, CSV) :

1. Exporter en CSV
2. Importer dans Airtable via l'interface (Add records → Import)
3. Mapper les colonnes vers les champs du schéma
