# CRM — Schéma et configuration

Le copilote utilise un CRM comme source de vérité de tes prospects et deals. 4 modes supportés : Airtable, Notion, NocoDB, ou un CRM custom.

## Choisir son CRM

| CRM | Pour qui | Setup | Guide |
|---|---|---|---|
| Airtable | Solo, simple, rapide | 5 min | [`docs/crm/airtable.md`](../docs/crm/airtable.md) |
| Notion | Déjà sur Notion | 10 min | [`docs/crm/notion.md`](../docs/crm/notion.md) |
| NocoDB | Self-hosted, open-source | 10 min | [`docs/crm/nocodb.md`](../docs/crm/nocodb.md) |
| Custom | Stack existante (HubSpot, Pipedrive...) | variable | [`docs/crm/custom.md`](../docs/crm/custom.md) |

## Schéma commun

Quel que soit le CRM choisi, la table `Prospects` doit contenir ces champs :

| Champ | Type | Notes |
|---|---|---|
| Name | Texte | Prénom + nom du prospect |
| Poste | Texte | Titre actuel |
| Boîte | Texte | Nom de l'entreprise |
| LinkedIn URL | URL | Lien profil LinkedIn |
| Statut pipeline | Select | Pool / Invitation / Connecté / Setting / RDV pris / Proposition / Client / Perdu |
| Signal d'achat | Texte long | Pourquoi qualifié maintenant |
| Score chaleur | Select | Froid / Tiède / Chaud / Prêt |
| Date dernière action | Date | |
| Notes | Texte long | |

## Configuration

Ajoute dans ton `.env` :

- `CRM_TYPE=` (airtable / notion / nocodb / custom)
- Les variables spécifiques au CRM choisi (voir le guide correspondant)

## Comportement attendu

Le copilote :

- **Lit** le CRM avant chaque routine pour connaître l'état du pipeline
- **Crée** des nouveaux prospects quand tu lances "Trouve-moi des prospects"
- **Update** les statuts à chaque action (envoi, réponse, RDV pris...)
- **N'écrit jamais sans ton accord** — il propose, tu valides

## Opérations logiques

Les skills utilisent ces opérations, indépendamment du CRM :

| Opération | Usage |
|---|---|
| Lister par statut | Pipeline snapshot (briefing, bilan) |
| Filtrer par date d'action | Follow-ups dus (relances, briefing) |
| Chercher par nom / LinkedIn URL | Matcher un prospect, éviter les doublons |
| Créer un prospect | Nouveau lead (prospection) |
| Mettre à jour un prospect | Après chaque action (statut, notes, date) |
| Compter par statut | KPIs (bilan hebdo) |

## Règles

1. **CRM = source de vérité.** Ne jamais deviner, toujours lire le CRM.
2. **Vérifier les doublons** avant de créer un prospect (chercher par LinkedIn URL).
3. **Inclure le profil LinkedIn** dès qu'il est disponible.
4. **Mettre à jour après chaque action** : Statut pipeline, Date dernière action, Notes.
