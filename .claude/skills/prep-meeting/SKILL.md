---
name: prep-meeting
description: |
  Prepare un RDV discovery ou commercial avec un prospect.
  Compile le profil, l'entreprise, les problemes pertinents,
  genere les questions discovery et un agenda structure.

  Triggers: "prepare mon RDV avec X", "prep meeting", "prepare le rendez-vous".
---

# Prep Meeting

Prepare un RDV avec un prospect en compilant toutes les infos disponibles.

## Input requis

L'utilisateur fournit au minimum UN de ces elements :
- Nom du prospect
- URL LinkedIn
- Nom de l'entreprise
- Page CRM du contact

## Process

### Etape 1 — Collecter les infos sur le prospect

1. **Chercher dans le CRM Notion** (database ID dans `.env`) :
   - Nom, entreprise, poste, statut, notes existantes
   - Historique des echanges (champ Notes, Dernier contact)

2. **Recherche web** sur le prospect et son entreprise :
   - Site de l'entreprise : services, equipe, positionnement, actualites
   - Profil LinkedIn du prospect (si URL disponible) : titre, experience, posts recents
   - Societe.com / Pappers : CA, effectif, date creation (si pertinent)

3. **Si Pack Pro actif (Unipile disponible)** — enrichir via LinkedIn API :
   - Profil complet : titre, experience, formation
   - Entreprise : taille, specialites
   - Posts recents du prospect (indices sur ses preoccupations)

### Etape 2 — Matcher avec la knowledge base

Lire les fichiers dans `knowledge/` pour preparer les angles :
- `knowledge/icp.md` : verifier que le prospect match le profil cible
- `knowledge/objections.md` : anticiper les objections probables
- `knowledge/pitch.md` : identifier les arguments les plus pertinents pour CE prospect

### Etape 3 — Generer le brief meeting

```markdown
# Brief Meeting — [Nom] / [Entreprise]
**Date** : [date du RDV]
**Duree** : [20 min / 45 min / 1h]
**Objectif** : [comprendre leurs douleurs / presenter l'offre / closer]

## Profil prospect
- **Nom** : [nom complet]
- **Poste** : [titre]
- **Entreprise** : [nom] — [ville], [X] salaries
- **Source** : [comment on l'a trouve]
- **Historique** : [echanges precedents]

## Contexte entreprise
- [infos cles trouvees en ligne]
- [actualites recentes si pertinentes]

## Hypotheses pre-meeting
1. [hypothese sur leur principal pain point]
2. [hypothese sur leur maturite par rapport a notre offre]
3. [hypothese sur leur budget/urgence]

## Questions discovery (dans l'ordre)

### Opener (2-3 min)
- "[question ouverte sur leur activite / actualite]"
- "[question sur leur organisation actuelle]"

### Explorer les douleurs (10-15 min)
- "[question sur le probleme principal qu'on resout]"
- "[question sur comment ils gerent ca aujourd'hui]"
- "[question sur les consequences / le cout du probleme]"
- "[question sur les tentatives passees de resolution]"

### Qualifier (5 min)
- "Si tu devais chiffrer [le probleme], ca represente combien en temps/argent ?"
- "C'est quoi le truc qui te ferait gagner le plus de temps demain ?"
- "C'est quoi le timing ? C'est urgent ou ca peut attendre ?"

### Tester la solution (3 min)
- "Si [notre solution] pouvait [benefice principal], tu l'utiliserais ?"
- "Qu'est-ce qui te bloquerait ?"
- "C'est quoi un budget acceptable pour resoudre ca ?"

## Objections anticipees et reponses
| Objection probable | Reponse preparee |
|--------------------|------------------|
| [Objection 1 depuis knowledge/objections.md] | [Reponse] |
| [Objection 2] | [Reponse] |
| [Objection 3] | [Reponse] |

## Next steps selon le resultat
- **Interesse** → [prochaine etape logique : demo, proposition, pilote]
- **Curieux mais pas pret** → [quoi envoyer + quand relancer]
- **Pas interesse** → noter les raisons dans le CRM, passer a "Perdu" ou "Nurturing"
```

### Etape 4 — Mettre a jour le CRM

- Ajouter les infos enrichies dans la fiche Notion du contact
- S'assurer que le statut et la date Next sont a jour

## Output

Afficher le brief complet et demander :
1. S'il veut ajuster des questions
2. La date/heure du RDV pour le noter dans le CRM

## Style

- Concis, actionnable
- Questions formulees dans le ton du fondateur (voir `knowledge/tone-of-voice.md`)
- Pas de jargon marketing sauf si le fondateur en utilise
