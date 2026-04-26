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

Le schéma est aligné avec le contrat décrit dans [`../../tools/crm.md`](../../tools/crm.md).

## Étape 3 — Partager la database avec l'intégration

1. Ouvre la database dans Notion
2. Clique sur "..." en haut à droite → "Add connections" → ajoute "GTM Copilot"
3. Récupère l'ID de la database depuis l'URL : `notion.so/<workspace>/<database_id>?v=...`
4. Copie le `<database_id>` (32 caractères, sans tirets)

## Étape 4 — Configurer `.env`

```
CRM_TYPE=notion
NOTION_API_KEY=secret_xxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Étape 5 — Vérifier

Lance le copilote dans Claude Code et demande-lui "liste les prospects au statut Pool". Si la connexion fonctionne, il te renvoie les lignes correspondantes. Sinon, vérifie que l'intégration est bien partagée avec la database (étape 3) — c'est l'erreur la plus fréquente.
