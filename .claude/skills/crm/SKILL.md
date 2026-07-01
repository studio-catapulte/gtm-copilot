---
name: crm
description: |
  Capacite CRM : le CRM est la source de verite du pipeline (prospects, statuts,
  deals). Skill-tool appele par les skills-process (daily, weekly, sourcing,
  prep-meeting) pour lire/ecrire le pipeline. L'outil concret (Notion, Airtable,
  NocoDB, custom) est declare dans CLAUDE.md > Outils actifs.

  Triggers: /crm, "mon pipeline", "mes prospects", "le CRM", "statut pipeline".

  Ce skill n'est en general PAS invoque seul : c'est un socle reference par les
  routines. Aucune cle en dur : credentials dans .env.
---

# /crm — Capacite CRM

Ce skill-tool encapsule l'acces au CRM. Il contient **le contrat** (schema + operations,
stable quel que soit l'outil) et, inline, le **mapping de l'outil actif**. Les guides de
setup des autres CRM vivent dans `docs/crm/`. L'outil actif est declare dans
`CLAUDE.md > Outils actifs`.

## Outil actif

Declare dans `CLAUDE.md > Outils actifs`. Le mapping concret des operations de l'outil
actif est **inline plus bas** (section « Adapter actif »). Pour brancher / changer de
CRM : les guides de setup de chaque option (Notion, Airtable, NocoDB, custom) sont dans
`docs/crm/` ; recopie/adapte alors la section « Adapter actif » ci-dessous.

---

## Contrat (SSOT — ne pas diverger par adapter)

### Schema commun

La table `Prospects` contient ces champs, **identiques quel que soit l'outil** (un
adapter qui renomme ou omet un champ casse les routines) :

| Champ | Type | Notes |
|---|---|---|
| Name | Texte | Prenom + nom du prospect |
| Poste | Texte | Titre actuel |
| Boite | Texte | Nom de l'entreprise |
| LinkedIn URL | URL | Lien profil LinkedIn |
| Statut pipeline | Select | Pool / Invitation / Connecte / Setting / RDV pris / Proposition / Client / Perdu |
| Signal d'achat | Texte long | Pourquoi qualifie maintenant |
| Score chaleur | Select | Froid / Tiede / Chaud / Pret |
| Date derniere action | Date | |
| Notes | Texte long | |

Les **valeurs de Statut pipeline** (8 exactes ci-dessus) sont un contrat : `daily`
compte "Pool", `weekly` compte "Client". Un adapter ne doit pas les renommer.

### Operations logiques

Les skills-process utilisent ces operations, independamment de l'outil. Chaque
adapter les mappe sur son API/CLI/MCP.

| Operation | Usage |
|---|---|
| `list-by-status(statut)` | Snapshot pipeline (briefing, bilan) |
| `filter-by-action-date(avant)` | Follow-ups dus (relances) |
| `find(nom \| linkedin_url)` | Matcher un prospect, eviter les doublons |
| `create(champs)` | Nouveau lead (prospection) |
| `update(id, champs)` | Apres chaque action (statut, notes, date) |
| `count-by-status()` | KPIs (bilan hebdo) |

---

## Adapter actif — Notion (REST)

> Defaut fourni. Setup (integration, database id) : `docs/crm/notion.md`. Cle statique
> `NOTION_API_KEY` → **headless-safe** (convient aux routines cron). API
> `https://api.notion.com/v1`, headers : `Authorization: Bearer $NOTION_API_KEY`,
> `Notion-Version: 2022-06-28`, `Content-Type: application/json`.

Mapping des operations du contrat :

- **`list-by-status` / `filter-by-action-date`** → `POST /databases/$NOTION_DATABASE_ID/query` avec filtre :
  ```bash
  curl -s -X POST "https://api.notion.com/v1/databases/$NOTION_DATABASE_ID/query" \
    -H "Authorization: Bearer $NOTION_API_KEY" -H "Notion-Version: 2022-06-28" \
    -H "Content-Type: application/json" \
    -d '{"filter":{"property":"Statut pipeline","select":{"equals":"Pool"}}}'
  ```
  Date (follow-ups) : `{"filter":{"property":"Date derniere action","date":{"on_or_before":"2026-07-01"}}}`.
- **`find`** → meme endpoint, filtre `LinkedIn URL` (`{"property":"LinkedIn URL","url":{"equals":"..."}}`) — chercher par URL d'abord pour la dedup.
- **`create`** → `POST /pages` :
  ```bash
  curl -s -X POST "https://api.notion.com/v1/pages" \
    -H "Authorization: Bearer $NOTION_API_KEY" -H "Notion-Version: 2022-06-28" \
    -H "Content-Type: application/json" \
    -d '{"parent":{"database_id":"'"$NOTION_DATABASE_ID"'"},"properties":{
        "Name":{"title":[{"text":{"content":"Jane Doe"}}]},
        "Statut pipeline":{"select":{"name":"Pool"}},
        "LinkedIn URL":{"url":"https://linkedin.com/in/janedoe"}}}'
  ```
- **`update`** → `PATCH /pages/<page_id>` avec le sous-objet `properties` a modifier.
- **`count-by-status`** → paginer la query (100/page, suivre `next_cursor`) et compter par valeur de `Statut pipeline`.

Types Notion : `Name`=title, selects=`select.name`, URL=`url`, Date=`date.start`,
textes longs=`rich_text`. Une valeur de Statut hors des 8 du contrat = rejet API.

## Regles

1. **CRM = source de verite.** Ne jamais deviner, toujours lire le CRM.
2. **Verifier les doublons** avant `create` (chercher par LinkedIn URL).
3. **Inclure le profil LinkedIn** des qu'il est disponible.
4. **Mettre a jour apres chaque action** : Statut, Date derniere action, Notes.
5. **N'ecrit jamais sans accord** — proposer, l'utilisateur valide.
