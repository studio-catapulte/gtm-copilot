# Setup CRM NocoDB

Guide pas à pas pour configurer NocoDB comme source de vérité du pipeline. Pertinent si tu veux du self-hosted, sans lock-in vendor, ou si tu as déjà une instance NocoDB.

## Étape 1 — Choisir une instance

Deux options :

- **Self-hosted** : déployer NocoDB en Docker (`nocodb/nocodb` sur DockerHub) sur ton VPS, Hetzner, OVH, etc.
- **NocoDB Cloud** : créer un compte sur [nocodb.com](https://nocodb.com), plan gratuit pour démarrer.

## Étape 2 — Créer la base et la table Prospects

Dans NocoDB :

1. Créer une nouvelle base "CRM"
2. Créer une table "Prospects"
3. Ajouter les colonnes selon le même schéma que [Notion](./notion.md) :

| Colonne | Type | Notes |
|---|---|---|
| Name | SingleLineText | Nom du prospect |
| Poste | SingleLineText | |
| Boîte | SingleLineText | |
| LinkedIn URL | URL | |
| Statut pipeline | SingleSelect | Pool, Invitation, Connecté, Setting, RDV pris, Proposition, Client, Perdu |
| Signal d'achat | LongText | |
| Score chaleur | SingleSelect | Froid, Tiède, Chaud, Prêt |
| Date dernière action | Date | |
| Notes | LongText | |

Schéma aligné avec [`../../tools/crm.md`](../../tools/crm.md).

## Étape 3 — Générer un API token

1. Cliquer sur ton avatar en haut à droite → "Account Settings" → "Tokens"
2. "Create new token" — donner le nom "GTM Copilot"
3. Copier le token

## Étape 4 — Récupérer les IDs

- L'URL de l'instance (ex. `https://nocodb.exemple.fr` ou `https://app.nocodb.com`)
- L'ID de la table : visible dans l'URL quand tu ouvres la table, ou via l'API browser intégré.

## Étape 5 — Configurer `.env`

```
CRM_TYPE=nocodb
NOCODB_URL=https://nocodb.exemple.fr
NOCODB_TOKEN=xxxxx
NOCODB_TABLE_ID=mxxxxxxxxxxxxxx
```

## Étape 6 — Vérifier

Lance le copilote dans Claude Code et demande "liste les prospects". S'il répond une liste vide ou peuplée selon ta table, c'est OK. Sinon : vérifier le token (permissions data read/write) et l'URL (sans `/` final).
