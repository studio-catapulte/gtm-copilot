# Port CRM — Schéma et configuration

**Port** (contrat agnostique) : le copilote utilise un CRM comme source de vérité
de tes prospects et deals. Les skills parlent à ce port, jamais à un CRM en dur.

## Binding

```
CRM_PROVIDER=notion     # ou airtable, nocodb, custom, ...
```

Lire `CRM_PROVIDER`, puis suivre l'adapter correspondant dans
`providers/crm/<provider>.md`. Les adapters fournis (Notion / Airtable / NocoDB /
custom) sont des **exemples** : la liste est ouverte. Brancher un vrai CRM
(HubSpot, Attio, Folks, Pipedrive…) = écrire **1 fichier** `providers/crm/<x>.md`
qui mappe le schéma commun ci-dessous sur son API, et poser `CRM_PROVIDER=<x>`.

## Choisir son CRM (adapters exemples)

| CRM | Pour qui | Setup | Guide |
|---|---|---|---|
| Airtable | Solo, simple, rapide | 5 min | [`.claude/skills/_shared/providers/crm/airtable.md`](providers/crm/airtable.md) |
| Notion | Déjà sur Notion | 10 min | [`.claude/skills/_shared/providers/crm/notion.md`](providers/crm/notion.md) |
| NocoDB | Self-hosted, open-source | 10 min | [`.claude/skills/_shared/providers/crm/nocodb.md`](providers/crm/nocodb.md) |
| Custom | Stack existante (HubSpot, Pipedrive...) | variable | [`.claude/skills/_shared/providers/crm/custom.md`](providers/crm/custom.md) |

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

- `CRM_PROVIDER=` (airtable / notion / nocodb / custom)
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
