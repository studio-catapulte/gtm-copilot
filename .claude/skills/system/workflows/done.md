# /done — Cloture de session

Cloturer proprement la session de travail : log, sync CRM, commit.

---

## Etape 1 — Resume

Analyser la conversation et identifier :
1. **Ce qui a ete accompli** (actions realisees, messages envoyes, contacts MAJ)
2. **Decisions prises** (changements de strategie, nouveaux objectifs)
3. **Prochaines etapes** identifiees mais non realisees

---

## Etape 2 — MAJ objectifs

Lire `knowledge/objectifs.md`. Si des objectifs ont ete avances pendant la session :
- Mettre a jour la progression
- Cocher ce qui est fait
- Ajouter les nouveaux objectifs qui ont emerge

Si rien n'a change, ne pas toucher le fichier.

---

## Etape 3 — MAJ CRM

Verifier si des contacts ont ete discutes pendant la session sans etre mis a jour dans le CRM.
Si oui, lister les MAJ necessaires et les appliquer :
- Changement de statut
- Notes a ajouter
- Prochaine action (champ Next)

Si tout est deja a jour, passer.

---

## Etape 4 — Revue des erreurs

Analyser la conversation et identifier les **erreurs rencontrees** :
- Appels API echoues
- Outils qui n'ont pas marche
- Commandes qui ont necessite plusieurs tentatives

**Si des erreurs ont ete trouvees :**
1. Les exposer clairement
2. Pour chaque erreur : symptome, cause probable, contournement utilise
3. Demander a l'utilisateur s'il veut qu'on corrige maintenant ou plus tard
4. Ne PAS corriger automatiquement

**Si aucune erreur** : ne rien afficher.

---

## Etape 5 — Git commit + push

```bash
git add <fichiers modifies>
git commit -m "<resume concis de la session>"
git pull --rebase && git push
```

Ne PAS stager `.env` ou fichiers sensibles.
Message de commit en francais, concis.

**Si conflit au rebase** :
1. Lister les conflits
2. Resoudre intelligemment (garder les deux versions quand c'est dans des sections differentes)
3. Continuer le rebase
4. Ne JAMAIS `--force`

---

## Etape 6 — Confirmation

```
Session terminee !

## Accompli
- [action 1]
- [action 2]

## CRM
- [X contacts mis a jour] ou "Deja a jour"

## Erreurs
- [erreur + fix propose] ou "Aucune"

## Git
- Commit : [hash court] — [message]

## Prochaines etapes
- [ ] [TODO 1]
- [ ] [TODO 2]

A demain !
```

---

## Regles

1. **Concis** — pas de blabla, aller droit au but
2. **CRM = source de verite** — toujours synchroniser avant de cloturer
3. **Pas de correction auto** — exposer les erreurs, laisser l'utilisateur decider
4. **Git propre** — ne jamais push du sensible, ne jamais --force
