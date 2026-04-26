# Setup CRM custom

Squelette pour les fondateurs qui ont déjà un CRM en place (HubSpot, Pipedrive, Salesforce, ou un stack maison) et veulent que le copilote tape dedans plutôt que d'ouvrir un nouveau silo.

## Principe

Le copilote a besoin de trois opérations logiques, peu importe l'implémentation :

1. **Lister les prospects** (filtrable par statut, par date, par owner)
2. **Créer un prospect** (avec au minimum nom, entreprise, LinkedIn, statut)
3. **Mettre à jour un prospect** (statut, notes, score, date dernière action)

Tant que ces trois opérations sont accessibles, n'importe quel CRM peut être branché.

## Recommandation : exposer en REST avec auth Bearer

L'approche la plus simple et la plus portable :

- Trois endpoints REST : `GET /prospects`, `POST /prospects`, `PATCH /prospects/{id}`
- Authentification via header `Authorization: Bearer <token>`
- Réponses JSON alignées avec le schéma commun (voir [`../../tools/crm.md`](../../tools/crm.md))

Cette couche peut être :

- Une fonction serverless (Vercel, Cloudflare Workers, Supabase Edge Functions...) qui proxy ton CRM existant.
- Un mini service Express/FastAPI hébergé chez toi.
- Un workflow n8n qui expose un webhook auth-protégé.

## Variables `.env`

```
CRM_TYPE=custom
CRM_CUSTOM_API_URL=https://crm-bridge.exemple.fr
CRM_CUSTOM_API_KEY=xxxxx
```

Tu peux ajouter tes propres variables (par exemple `HUBSPOT_PORTAL_ID`, `PIPEDRIVE_DOMAIN`...) si ta couche bridge en a besoin.

## Intégration côté copilote

Pour brancher concrètement le copilote sur ta couche custom, parler avec Nefia : selon les volumes et la complexité, on adapte `tools/crm.md` ou on ajoute un client dédié dans `plugins/`. Ce squelette est un point de départ, pas un mode plug-and-play complet.
