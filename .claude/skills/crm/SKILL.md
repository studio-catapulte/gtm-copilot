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
stable quel que soit l'outil) et **les adapters** (comment faire concretement, un par
outil dans `adapters/`). L'outil actif est declare dans `CLAUDE.md > Outils actifs`.

## Provider actif

Lire `CLAUDE.md > Outils actifs` pour savoir quel CRM est branche, puis suivre son
adapter dans `adapters/<provider>.md` (mapping concret des operations ci-dessous +
setup). Adapters fournis : `notion`, `airtable`, `nocodb`, `custom`. En brancher un
autre (HubSpot, Attio, Folks…) = ecrire 1 fichier `adapters/<x>.md` qui mappe le
contrat ci-dessous, et le declarer dans CLAUDE.md.

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

## Regles

1. **CRM = source de verite.** Ne jamais deviner, toujours lire le CRM.
2. **Verifier les doublons** avant `create` (chercher par LinkedIn URL).
3. **Inclure le profil LinkedIn** des qu'il est disponible.
4. **Mettre a jour apres chaque action** : Statut, Date derniere action, Notes.
5. **N'ecrit jamais sans accord** — proposer, l'utilisateur valide.
