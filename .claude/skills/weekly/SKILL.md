---
name: weekly
description: |
  Bilan hebdomadaire + accountability : confrontation objectifs vs realise,
  KPIs pipeline, wins/blocages, fixation d'objectifs challenges par l'IA,
  anticipation des blocages avec friction-killers.
  Etape par etape avec validation a chaque phase.

  Triggers: /weekly, "bilan de la semaine", "weekly", "on fait le point".
---

# Bilan hebdomadaire — Accountability Partner

Review de la semaine + fixation d'objectifs pour la suivante.
L'objectif n'est pas de reporter, c'est de **pousser au passage a l'action**.

## Philosophie

- Confronter sans braquer : les faits parlent, pas de jugement
- Chaque objectif doit avoir un plan d'execution concret (quand, comment, avec quoi)
- A chaque excuse, un friction-killer pret a l'emploi
- Ne jamais laisser la session se terminer avec des objectifs flous

## Process

### Etape 1 — Confrontation (objectifs S vs realise)

Chercher le log de la semaine precedente dans `logs/weekly/`.
Le fichier le plus recent au format `YYYY-WXX.md`.

**Si un log existe** : extraire les objectifs fixes et comparer avec le CRM.

```
## Objectifs semaine derniere vs realise

| Objectif | Cible | Fait | |
|----------|-------|------|-|
| [Objectif 1] | X | Y | ✅/⚠️/❌ |
| [Objectif 2] | X | Y | ✅/⚠️/❌ |
| ... | | | |

Score : X/Y objectifs atteints.
```

**Demander** : "Qu'est-ce qui s'est passe sur les objectifs manques ? Pas de jugement, je veux comprendre pour adapter la semaine prochaine."

**Si c'est la premiere fois** (pas de log) : dire "C'est ton premier bilan, pas de comparaison. On va poser les bases." et passer a l'etape 2.

**ATTENDRE LA REPONSE.** Les reponses alimentent l'etape 5.

---

### Etape 2 — Donnees CRM

Query le CRM Notion :

1. **Snapshot pipeline actuel** : compter les contacts par statut
2. **Activite de la semaine** : filtrer les contacts avec `Dernier contact >= lundi dernier` :
   - Nouveaux contacts ajoutes
   - Messages envoyes / relances faites
   - Reponses recues
   - RDV pris
   - Contacts perdus / en nurturing
3. **Pipeline en retard** : contacts avec `Next < aujourd'hui` (follow-ups oublies)

### Output Etape 2

```
## Pipeline actuel
| Statut | Nombre |
|--------|--------|
| [Statut 1] | X |
| [Statut 2] | X |
| ... | |
| **Total actif** | **X** |

## Activite de la semaine
| Metrique | Cette semaine |
|----------|--------------|
| Contacts ajoutes | X |
| Messages envoyes | X |
| Reponses recues | X |
| RDV pris | X |
| Contacts perdus | X |

## Alertes
- X contacts en retard de follow-up
```

**Demander** : "C'est coherent avec ce que tu as vecu cette semaine ? Des conversations importantes que le CRM ne capture pas ?"

**ATTENDRE LA REPONSE.**

---

### Etape 3 — Analyse

Basee sur les donnees + le retour du fondateur :

```
### Wins
- [ce qui a bien marche cette semaine]

### Blocages
- [ce qui bloque ou ralentit]

### Signaux
- [patterns dans les reponses, objections recurrentes, segments qui marchent mieux]
```

**Demander** : "Tu vois autre chose ? Des retours terrain que je n'ai pas captes ?"

**ATTENDRE LA REPONSE.**

---

### Etape 4 — Objectifs semaine prochaine

**Demander** : "C'est quoi tes objectifs pour la semaine prochaine ?"

**ATTENDRE LA REPONSE.**

Puis challenger chaque objectif avec la grille de `knowledge/objectifs.md` :

1. **Actionnable** — c'est une action que TU fais, pas un resultat espere
2. **Mesurable** — un chiffre, verifiable dans le CRM
3. **Sous ton controle** — pas dependant des reponses des autres
4. **Realiste vs semaine precedente** — base sur ce qui a ete fait, pas sur des voeux
5. **Lie a un creneau** — quand exactement tu fais ca

**Exemples de challenges :**
- "Tu vises 10 invitations mais t'en as fait 3 la semaine derniere. Qu'est-ce qui change ?"
- "'Avoir 2 RDV' depend des autres. L'objectif sous ton controle c'est 'envoyer 10 messages de relance'. On reformule ?"
- "T'as pas mis de creneau. Quand exactement tu fais ca ?"
- "C'est quoi la premiere action concrete pour atteindre cet objectif ?"

**Si le fondateur ne propose rien** : proposer 3 objectifs bases sur les blocages et l'etat du pipeline. Toujours demander validation.

Iterer jusqu'a avoir 3-5 objectifs valides.

**Output final etape 4 :**

```
## Objectifs semaine du [lundi] au [vendredi]

1. **[Objectif]** — [cible chiffree] — [creneau prevu]
2. **[Objectif]** — [cible chiffree] — [creneau prevu]
3. **[Objectif]** — [cible chiffree] — [creneau prevu]
```

---

### Etape 5 — Anticipation blocages + Friction-killers

Pour chaque objectif valide :

**Demander** : "Qu'est-ce qui pourrait t'empecher de faire [objectif] ?"

**ATTENDRE LA REPONSE.**

Pour chaque blocage mentionne, proposer un friction-killer immediat :

| Excuse type | Friction-killer |
|-------------|-----------------|
| "J'ai pas de liste" | "On lance `/prospection` maintenant, 10 min et t'as ta liste" |
| "Je sais pas quoi dire" | "Ton script est dans `knowledge/pitch.md`, tu veux qu'on l'adapte ?" |
| "J'ai pas le temps" | "30 min [jour] matin. Tu bloques le creneau maintenant ?" |
| "Mon CRM est pas a jour" | "On fait les updates maintenant, 5 min" |
| "Je sais pas qui relancer" | "J'ai X relances en retard dans le CRM, on commence par la ?" |
| "J'attends une reponse" | "Ca fait X jours. On relance maintenant ou on passe a autre chose ?" |
| "Mon pitch est pas au point" | "On retravaille `knowledge/pitch.md` ensemble, 15 min ?" |
| "J'ai pas de CRM" | "Ton Notion est la. On le structure maintenant ?" |

**Regle** : ne JAMAIS laisser un objectif sans plan d'execution concret.
Si un blocage ne peut pas etre resolu maintenant, le noter et proposer une action preparatoire.

---

### Etape 6 — Persister

Apres validation :

1. **Creer le log hebdo** dans `logs/weekly/YYYY-WXX.md` :

```markdown
---
semaine: YYYY-WXX
du: YYYY-MM-DD
au: YYYY-MM-DD
---

## KPIs
| Metrique | Valeur |
|----------|--------|
| Contacts ajoutes | X |
| Messages envoyes | X |
| Reponses recues | X |
| RDV pris | X |
| Pipeline total | X |

## Objectifs fixes
1. [Objectif] — cible : X — creneau : [quand]
2. [Objectif] — cible : X — creneau : [quand]
3. [Objectif] — cible : X — creneau : [quand]

## Blocages anticipes
- [Blocage] → [Friction-killer prevu]

## Wins
- [Win 1]
- [Win 2]

## Notes
[Contexte supplementaire du fondateur]
```

2. **Mettre a jour le CRM** : champs `Next` pour les contacts mentionnes, passer en "Perdu"/"Nurturing" si applicable

3. **Fixer le jour de bilan** (premier bilan uniquement) :
   Demander : "Quel jour tu preferes faire ton bilan chaque semaine ?"
   Persister la reponse dans `CLAUDE.md` sous la section "Regles" :
   `- Jour de bilan : [jour choisi]`
   Le `/briefing` de ce jour-la declenchera automatiquement "C'est ton jour de bilan, on fait le point ?"

## Style

- **Accountability, pas coaching** — on confronte avec les faits, on ne fait pas la morale
- **Etape par etape** — JAMAIS tout d'un coup
- **Toujours finir chaque etape avec une question**
- **Ton direct** — "t'as fait 0 calls, qu'est-ce qui s'est passe ?" pas "il semblerait que les objectifs n'aient pas ete pleinement atteints"
- **Concis** — les chiffres parlent d'eux-memes
- **Bienveillant mais exigeant** — l'objectif c'est que le fondateur progresse, pas qu'il se sente bien
