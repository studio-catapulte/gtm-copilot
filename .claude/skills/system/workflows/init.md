# /system init — Setup guide du copilote

Guide l'utilisateur pas a pas pour configurer son copilote.
A utiliser UNE SEULE FOIS, a l'installation du repo.

## Prerequis

Avant de commencer, verifier :
1. Le repo est clone en local
2. `.env` existe (copie de `.env.example`)
3. Claude Code est installe et fonctionne

Si un prerequis manque, guider l'utilisateur pour le resoudre avant de continuer.

---

## Etape 1 — Identite (CLAUDE.md)

Poser les questions une par une. **ATTENDRE la reponse entre chaque question.**

1. "Comment tu t'appelles ?"
2. "C'est quoi ta boite ? En 2-3 phrases."
3. "Tu vends quoi, et a qui ?"
4. "Qu'est-ce qui te differencie de tes concurrents ?"

Remplir les placeholders correspondants dans `CLAUDE.md` :
- `[PRENOM]`, `[ENTREPRISE]`, `[DESCRIPTION EN 2-3 PHRASES]`
- `[OFFRE PRINCIPALE]`, `[TYPE DE CLIENT]`, `[1-2 DIFFERENCIATEURS]`

Montrer le resultat et demander validation.

---

## Etape 2 — Cible (CLAUDE.md + knowledge/icp.md)

1. "C'est qui ton client ideal ? Son titre, la taille de sa boite, son secteur ?"
2. "Quels sont les signaux qui te disent qu'un prospect est chaud ?"
3. "Qui tu ne veux SURTOUT PAS cibler ?"

Remplir :
- Section "Notre cible" dans `CLAUDE.md`
- `knowledge/icp.md` avec le detail

Montrer le resultat et demander validation.

---

## Etape 3 — Process de vente (CLAUDE.md)

1. "C'est quoi tes etapes de vente, du premier contact jusqu'a la signature ?"
2. "Tu relances combien de fois max avant de lacher ?"
3. "C'est quoi tes criteres pour qualifier un prospect ?"

Remplir la section "Notre process de vente" dans `CLAUDE.md`.

Si l'utilisateur ne sait pas, proposer un pipeline par defaut :
`Pool → Invitation → Connecte → Setting → RDV pris → Proposition → Client / Perdu`

Montrer le resultat et demander validation.

---

## Etape 4 — Ton et style (CLAUDE.md + knowledge/tone-of-voice.md)

1. "Tu tutoies ou tu vouvoies tes prospects ?"
2. "Ton style c'est plutot formel, decontracte, direct ?"
3. "Colle-moi un vrai message que t'as envoye a un prospect (premier contact, relance, ou proposition)"

Remplir :
- Section "Comment je parle" dans `CLAUDE.md`
- `knowledge/tone-of-voice.md` avec les exemples

**Minimum 1 exemple reel obligatoire.** Si l'utilisateur n'en a pas, lui demander d'en ecrire un maintenant.

Montrer le resultat et demander validation.

---

## Etape 5 — Pitch et objections (knowledge/)

1. "En 30 secondes, c'est quoi ton pitch ? (comme si t'etais au tel avec un prospect)"
2. "C'est quoi les 3 objections que t'entends le plus souvent ?"
3. "Et tu reponds quoi a chacune ?"

Remplir :
- `knowledge/pitch.md`
- `knowledge/objections.md`

Montrer le resultat et demander validation.

---

## Etape 6 — CRM

1. "Tu utilises quoi comme CRM ? (Notion, Airtable, NocoDB, autre)"
2. Selon la reponse, guider le remplissage de `tools/crm.md` et `.env`
3. **Tester la connexion** : lancer une requete de lecture sur le CRM
   - Si ca marche : "CRM connecte, tout est bon"
   - Si ca echoue : diagnostiquer (cle API manquante, URL incorrecte, permissions), aider a corriger, retester

---

## Etape 7 — Outils externes

1. "T'as un compte Unipile pour LinkedIn/email ?" (si le plugin est present)
   - Si oui : verifier `.env` (UNIPILE_DSN, UNIPILE_API_KEY), tester la connexion
   - Si non : "Pas de souci, les commandes LinkedIn/email seront desactivees. Tu pourras les activer plus tard."

Pour chaque outil, tester la connexion et reporter le statut.

---

## Etape 8 — Test de sante

Lancer un mini-test pour valider que tout fonctionne :

1. **CRM** : lire 1 contact (ou creer un contact test si le CRM est vide)
2. **LinkedIn** (si active) : chercher 1 profil correspondant a l'ICP
3. **Email** (si active) : lister les 3 derniers mails

Afficher :

```
## Test de sante

| Outil | Statut |
|-------|--------|
| CRM ([type]) | OK / Erreur : [detail] |
| LinkedIn | OK / Desactive / Erreur : [detail] |
| Email | OK / Desactive / Erreur : [detail] |
```

Si tout est OK, passer a l'etape suivante. Sinon, proposer de corriger maintenant.

---

## Etape 9 — Premier commit

```bash
git add -A
git commit -m "init: configuration copilote [ENTREPRISE]"
git push
```

---

## Etape 10 — Recap

```
Copilote configure !

## Ton setup
- Entreprise : [ENTREPRISE]
- Cible : [TITRE] dans [SECTEUR], [TAILLE]
- Pipeline : [ETAPES]
- CRM : [TYPE] — connecte
- LinkedIn : [active/desactive]
- Email : [active/desactive]

## Tes commandes
| Dis ca | Quand |
|--------|-------|
| "Routine du matin" | Chaque matin (30-40 min) |
| "Prepare mon RDV avec X" | Avant un meeting (5 min) |
| "Weekly" | Bilan de la semaine (15 min) |
| "Trouve-moi des prospects" | Quand le pipeline est vide (15 min) |
| "Fais des slides pour X" | Avant un RDV important (10 min) |
| "/done" | Fin de session |

## Prochaine etape
Lance "Routine du matin" pour ta premiere session !
```

---

## Regles

1. **Etape par etape** — JAMAIS tout d'un coup, toujours attendre la reponse
2. **Idempotent** — relancer `/system init` ne doit pas casser ce qui est deja configure (demander avant d'ecraser)
3. **Pas d'invention** — si un outil ne marche pas, dire "ca marche pas" et aider a corriger
4. **Validation humaine** — montrer le resultat de chaque etape, attendre "ok" avant de continuer
