# Setup CRM Notion

Guide pas à pas pour configurer Notion comme source de vérité du pipeline du copilote. Recommandé si tu utilises déjà Notion au quotidien.

## Étape 1 — Créer une intégration Notion

1. Va sur [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Clique "New integration", donne-lui le nom "GTM Copilot"
3. Choisis l'espace de travail concerné
4. Copie le "Internal Integration Token" (commence par `secret_...`) — on en aura besoin à l'étape 4

## Étape 2 — Créer la base de données Prospects

Crée une page dans Notion contenant une database (full page ou inline) avec ces propriétés :

| Propriété | Type | Notes |
|---|---|---|
| Name | Title | Nom du prospect |
| Poste | Text | |
| Boîte | Text | Nom de l'entreprise |
| LinkedIn URL | URL | |
| Statut pipeline | Select | Pool, Invitation, Connecté, Setting, RDV pris, Proposition, Client, Perdu |
| Signal d'achat | Text | Pourquoi qualifié maintenant |
| Score chaleur | Select | Froid, Tiède, Chaud, Prêt |
| Date dernière action | Date | |
| Notes | Text | |

Le schéma est aligné avec le contrat décrit dans [`../SKILL.md`](../SKILL.md).

## Étape 3 — Partager la database avec l'intégration

1. Ouvre la database dans Notion
2. Clique sur "..." en haut à droite → "Add connections" → ajoute "GTM Copilot"
3. Récupère l'ID de la database depuis l'URL : `notion.so/<workspace>/<database_id>?v=...`
4. Copie le `<database_id>` (32 caractères, sans tirets)

## Étape 4 — Configurer `.env` + CLAUDE.md

`.env` (secrets uniquement) :

```
NOTION_API_KEY=secret_xxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

`CLAUDE.md > Outils actifs` (le choix d'outil, lu par l'agent) :

```
- CRM : Notion (adapter notion, REST) — voir skills/crm/
```

## Étape 5 — Vérifier

Demande au copilote "liste les prospects au statut Pool". Si ça marche, il renvoie
les lignes. Sinon, vérifie que l'intégration est partagée avec la database (étape 3)
— l'erreur la plus fréquente.

---

## Mapping des opérations (Notion REST)

Concret pour chaque opération du contrat (`../SKILL.md`). API `https://api.notion.com/v1`,
headers : `Authorization: Bearer $NOTION_API_KEY`, `Notion-Version: 2022-06-28`,
`Content-Type: application/json`. Adapter **headless-safe** (clé statique, pas d'OAuth
interactif) → convient aux routines cron.

**`list-by-status(statut)`** et **`filter-by-action-date(avant)`** → `POST /databases/$NOTION_DATABASE_ID/query` avec un filtre :

```bash
curl -s -X POST "https://api.notion.com/v1/databases/$NOTION_DATABASE_ID/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"filter":{"property":"Statut pipeline","select":{"equals":"Pool"}}}'
```

Filtre date (follow-ups dus) : `{"filter":{"property":"Date derniere action","date":{"on_or_before":"2026-07-01"}}}`.

**`find(nom | linkedin_url)`** → même endpoint, filtre sur `LinkedIn URL` (`{"property":"LinkedIn URL","url":{"equals":"..."}}`) ou `Name` (`{"property":"Name","title":{"contains":"..."}}`). Toujours chercher par LinkedIn URL d'abord pour la dédup.

**`create(champs)`** → `POST /pages` :

```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"parent":{"database_id":"'"$NOTION_DATABASE_ID"'"},"properties":{
      "Name":{"title":[{"text":{"content":"Jane Doe"}}]},
      "Statut pipeline":{"select":{"name":"Pool"}},
      "LinkedIn URL":{"url":"https://linkedin.com/in/janedoe"}}}'
```

**`update(id, champs)`** → `PATCH /pages/<page_id>` avec le sous-objet `properties` à modifier (ex. `{"properties":{"Statut pipeline":{"select":{"name":"RDV pris"}},"Date derniere action":{"date":{"start":"2026-07-01"}}}}`).

**`count-by-status()`** → paginer `POST /databases/.../query` (100/page, suivre `next_cursor`) et compter côté client par valeur de `Statut pipeline`.

> Types de propriétés Notion à respecter : `Name`=title, selects=`select.name`, URL=`url`,
> Date=`date.start`, textes longs=`rich_text`. Une valeur de Statut hors des 8 du contrat
> = rejet API.
