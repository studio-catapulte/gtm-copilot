# Setup GTM Copilot

Quickstart fondateur : ~15 min, du `git clone` à la première routine du matin.

## Pré-requis

- [Claude Code](https://claude.ai) installé (abonnement Claude Pro, 20 EUR/mois).
- Un compte Unipile (le lien d'inscription et les clés d'accès te sont fournis par Nefia).
- Un CRM choisi parmi : Airtable, Notion, NocoDB, ou ton propre stack (HubSpot, Pipedrive, custom...).
- Python 3 disponible sur ta machine (pour les scripts `plugins/unipile/`).

## Étape 1 — Cloner et configurer

```bash
git clone https://github.com/studio-catapulte/gtm-copilot.git
cd gtm-copilot
cp .env.example .env
```

Puis installer le venv Python pour les scripts Unipile :

```bash
cd plugins/unipile && ./setup.sh
cd ../..
```

## Étape 2 — Choisir et configurer ton CRM

Le CRM est la source de vérité du copilote. Choisis-en un et suis le guide correspondant :

- Airtable (par défaut, gratuit, le plus simple) → [`crm/airtable.md`](./crm/airtable.md)
- Notion (si tu utilises déjà Notion) → [`crm/notion.md`](./crm/notion.md)
- NocoDB (self-hosted, pas de lock-in) → [`crm/nocodb.md`](./crm/nocodb.md)
- Custom — HubSpot, Pipedrive, ton propre stack → [`crm/custom.md`](./crm/custom.md)

À la fin de cette étape, les variables CRM (`CRM_TYPE`, `AIRTABLE_*` / `NOTION_*` / etc.) sont remplies dans `.env`.

## Étape 3 — Connecter LinkedIn et email

Nefia te fournit trois valeurs à coller dans `.env` :

- `UNIPILE_DSN` — l'endpoint de ton tenant Unipile.
- `UNIPILE_API_KEY` — la clé API Unipile.
- `UNIPILE_ACCOUNT_ID` — récupéré après que tu aies cliqué sur le lien OAuth que Nefia t'envoie (Outlook, Gmail, et/ou LinkedIn selon ton pack).

Côté fondateur, ton seul geste : cliquer le lien OAuth, accepter les permissions Microsoft / Google / LinkedIn, et confirmer à Nefia une fois fait. Le détail technique côté Nefia est dans [`operators/`](./operators/README.md).

## Étape 4 — Personnaliser le copilote

Ouvre Claude Code dans le dossier `gtm-copilot/` et tape :

```
/system init
```

Le copilote te pose les questions une par une (qui tu es, ce que tu vends, à qui, ton ton, ton pitch, tes objections) et remplit `CLAUDE.md` + les fichiers de `knowledge/` (`pitch.md`, `icp.md`, `objections.md`, `tone-of-voice.md`) à ta place. Compte ~10 à 15 minutes selon le niveau de détail que tu fournis.

Tu peux aussi remplir manuellement si tu préfères : édite `CLAUDE.md` (placeholders) et les 4 fichiers de `knowledge/`.

## Étape 5 — Lancer

Toujours dans Claude Code, dis simplement :

```
Routine du matin
```

Le copilote va checker ton inbox, lister les nouvelles connexions LinkedIn, te suggérer des relances et préparer tes invitations. Rien ne part sans ton accord explicite.

## Et après ?

Les autres commandes utiles sont listées dans le [`README.md`](../README.md) à la racine. Pour comprendre comment le copilote utilise ton CRM en interne, voir [`tools/crm.md`](../tools/crm.md).
