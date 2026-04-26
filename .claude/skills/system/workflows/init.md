# /system init — Setup guide du copilote

Guide l'utilisateur pas a pas pour configurer son copilote.
A utiliser UNE SEULE FOIS, a l'installation du repo.

Trigger officiel : `/system init`. Pas `/init`, pas `/system` seul.

## Prerequis

Avant de commencer, verifier :
1. Le repo est clone en local
2. `.env` existe (copie de `.env.example`)
3. Claude Code est installe et fonctionne

Si un prerequis manque, guider l'utilisateur pour le resoudre avant de continuer.

---

## Etape 0 — Pointeurs (gain de temps)

Avant de te poser les questions une par une, donne-moi ce que tu as deja sous la main. Je m'en sers pour pre-remplir un brouillon, et je ne te poserai des questions que sur les trous.

Demande au fondateur :

1. **URL de ton profil LinkedIn** (recommande) — je recupere ton parcours, ton positionnement actuel, ta headline.
2. **URL de ton site web ou de ta landing page** (si dispo) — je recupere ton pitch, ton offre, ton ton.
3. **Un PDF, un Notion, ou un Google Doc avec ton offre / deck commercial** (colle le contenu ou un lien public) — je l'utilise pour le pricing, le packaging, les differenciateurs.
4. **3 a 5 DMs LinkedIn recents** que tu as envoyes (colle-les) — je m'en sers pour calibrer ton ton.

**Si l'utilisateur dit "j'ai rien" :** OK, on passe directement a l'etape 1. Pas de blocage.

**Si l'utilisateur fournit au moins le LinkedIn :**

1. Utilise `WebFetch` sur l'URL LinkedIn fournie. Extrais : nom, headline, entreprise actuelle, parcours resume.
2. Si site web fourni : `WebFetch` la home + page "A propos" / "Pricing" / "Offre". Extrais : pitch principal, offre, prix si visible, differenciateurs.
3. Si doc commercial colle : lis le contenu. Extrais : offre principale, tiers de pricing, temoignages, garanties.
4. Si DMs colles : analyse le ton (tutoiement / vouvoiement, longueur, formules d'ouverture, presence/absence de tirets, emojis, etc.).
5. Construis un **brouillon mental** des sections de `CLAUDE.md` + des fichiers `knowledge/`. Ne l'ecris PAS encore.

Puis, **presente le brouillon** au fondateur sous cette forme :

> "Voila ce que j'ai compris de toi a partir de [LinkedIn + site] :
>
> - Tu es [nom], [titre], chez [boite].
> - Tu vends [offre deduite] a [cible deduite].
> - Ton positionnement : [phrase deduite].
> - Ton ton (depuis tes DMs) : [vouvoiement / tutoiement, formel / decontracte, presence de tirets].
> - Ton pitch (depuis ton site) : [extrait reformule].
>
> Je te confirme tout ca en te posant des questions ciblees dans les etapes suivantes. Tu pourras corriger / valider a chaque etape. Pret ?"

Une fois le fondateur OK, passe a l'etape 1, mais en mode **validation rapide** plutot que question ouverte si tu as deja la reponse.

**Important** : le scraping passe par `WebFetch` (outil natif Claude Code). Pas de scraper Python custom, pas de service tiers.

---

## Etape 1 — Identite (CLAUDE.md)

**Si l'etape 0 a fourni des donnees :** presente le brouillon deduit (nom, boite, offre, differenciateurs) et demande "tu confirmes ou tu corriges ?" au lieu de poser la question ouverte. Pose les questions ouvertes uniquement sur les champs vides.

Sinon, poser les questions une par une. **ATTENDRE la reponse entre chaque question.**

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

**Si l'etape 0 a fourni des donnees :** propose un brouillon de cible (titre, taille, secteur) deduit du LinkedIn et du site, puis demande "tu confirmes ou tu corriges ?". Garde les questions ouvertes pour les signaux d'achat et les anti-profils, qui sont rarement explicites en ligne.

1. "C'est qui ton client ideal ? Son titre, la taille de sa boite, son secteur ?"
2. "Quels sont les signaux qui te disent qu'un prospect est chaud ?"
3. "Qui tu ne veux SURTOUT PAS cibler ?"

Remplir :
- Section "Notre cible" dans `CLAUDE.md`
- `knowledge/icp.md` avec le detail

Montrer le resultat et demander validation.

---

## Etape 3 — Process de vente (CLAUDE.md)

**Si l'etape 0 a fourni des donnees :** rare que le process apparaisse en ligne. Pose les questions normalement.

1. "C'est quoi tes etapes de vente, du premier contact jusqu'a la signature ?"
2. "Tu relances combien de fois max avant de lacher ?"
3. "C'est quoi tes criteres pour qualifier un prospect ?"

Remplir la section "Notre process de vente" dans `CLAUDE.md`.

Si l'utilisateur ne sait pas, proposer un pipeline par defaut :
`Pool → Invitation → Connecte → Setting → RDV pris → Proposition → Client / Perdu`

Montrer le resultat et demander validation.

---

## Etape 4 — Ton et style (CLAUDE.md + knowledge/tone-of-voice.md)

**Si l'etape 0 a fourni des DMs :** propose un brouillon du ton (tutoiement/vouvoiement, niveau de formalite, regles de style detectees comme "pas de tirets" ou "phrases courtes") et demande "tu confirmes ou tu corriges ?". Reutilise un des DMs colles comme exemple "premier contact" si pertinent. Pose les questions ouvertes uniquement pour les exemples manquants (relance, proposition).

Sinon :

1. "Tu tutoies ou tu vouvoies tes prospects ?"
2. "Ton style c'est plutot formel, decontracte, direct ?"
3. "Colle-moi un vrai message que t'as envoye a un prospect (premier contact, relance, ou proposition)"

Remplir :
- Section "Comment je parle" dans `CLAUDE.md`
- `knowledge/tone-of-voice.md` avec les exemples

**Minimum 1 exemple reel obligatoire.** Si l'utilisateur n'en a pas, lui demander d'en ecrire un maintenant.

Montrer le resultat et demander validation.

---

## Etape 5 — Strategie et offre (knowledge/)

Cette etape remplit `knowledge/pitch.md`, `knowledge/objections.md`, ET `knowledge/strategy.md` (le fichier strategique au-dessus de l'offre).

**Si l'etape 0 a fourni un site ou un deck :** pour chaque sous-question, **propose un brouillon deduit** (pricing, tiers, packaging, differenciateurs, garanties...) et demande validation/correction au lieu de partir d'une page blanche. Pose les questions ouvertes uniquement sur les champs vides.

### Q5.1 — Pitch 30 secondes

"En 30 secondes, c'est quoi ton pitch ? (comme si t'etais au tel avec un prospect)"

### Q5.2 — Positioning vs concurrents

"Cite-moi 3 alternatives a ton offre du point de vue d'un prospect : 2 concurrents directs (ou faux amis), et le statu quo (ce qu'il fait aujourd'hui sans toi). Pour chacun, qu'est-ce qu'il fait mieux que toi, et qu'est-ce que toi tu fais mieux que lui ?"

### Q5.3 — Packaging

"Comment tu emballes ton offre ? Liste tes tiers / SKUs : pour qui, ce qui est inclus, le prix, la duree d'engagement. Tes add-ons eventuels."

### Q5.4 — Buying committee

"Dans une boite cible typique, qui decide d'acheter ton offre ? Qui paie ? Qui s'en sert au quotidien ? Y a-t-il un influenceur (associe, RH, opex) qui peut freiner ou faciliter ?"

### Q5.5 — Land-expand

"Comment tu rentres typiquement chez un client (land : ticket d'entree, duree) ? Et comment tu fais grossir le compte ensuite (expand : prochaines etapes naturelles) ?"

### Q5.6 — Pricing rationale

"Pourquoi tes prix sont ce qu'ils sont ? A quoi tu te compares (alternatives, salaires de remplacants, ROI attendu) ? Quelle est ta politique de reduction ?"

### Q5.7 — 3 objections les plus frequentes

"C'est quoi les 3 objections que t'entends le plus souvent ?"

### Q5.8 — Tes reponses a chaque objection

"Et tu reponds quoi a chacune ?"

### Generation

A partir des reponses, remplis :
- `knowledge/pitch.md` (Q5.1, plus differenciateurs et arguments cles deduits si non explicites)
- `knowledge/strategy.md` (Q5.2 a Q5.6, plus garanties et lignes rouges si l'utilisateur en a mentionne)
- `knowledge/objections.md` (Q5.7, Q5.8)

Montrer le resultat et demander validation.

---

## Etape 6 — CRM

1. "Tu utilises quoi comme CRM ? (Airtable, Notion, NocoDB, ou un CRM existant style HubSpot/Pipedrive/Salesforce a brancher en custom)"

2. Selon la reponse, **set la variable `CRM_TYPE` dans `.env`** :
   - Airtable → `CRM_TYPE=airtable`
   - Notion → `CRM_TYPE=notion`
   - NocoDB → `CRM_TYPE=nocodb`
   - Custom (HubSpot, Pipedrive, Salesforce, autre) → `CRM_TYPE=custom`

3. **Pointer le fondateur vers le guide correspondant** dans `docs/crm/` :
   - Airtable → `docs/crm/airtable.md`
   - Notion → `docs/crm/notion.md`
   - NocoDB → `docs/crm/nocodb.md`
   - Custom → `docs/crm/custom.md`

4. **Demander de remplir les variables `.env`** correspondantes (decommenter le bloc concerne dans `.env.example` puis remplir dans `.env`) :
   - Airtable : `AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`, `AIRTABLE_TABLE_ID`
   - Notion : `NOTION_API_KEY`, `NOTION_DATABASE_ID`
   - NocoDB : `NOCODB_URL`, `NOCODB_TOKEN`, `NOCODB_TABLE_ID`
   - Custom : `CRM_CUSTOM_API_URL`, `CRM_CUSTOM_API_KEY`

5. **Mettre a jour la section CRM dans `CLAUDE.md`** : remplacer `Outil : **[CRM_TYPE]** — \`[airtable | notion | nocodb | custom]\`` par le vrai type choisi (par exemple `Outil : **airtable**`).

6. **Tester la connexion** : lancer une requete de lecture sur le CRM
   - Si ca marche : "CRM connecte, tout est bon"
   - Si ca echoue : diagnostiquer (cle API manquante, URL incorrecte, permissions), aider a corriger, retester

---

## Etape 7 — Outils externes

1. "T'as un compte Unipile pour LinkedIn/email ?" (si le plugin est present)
   - Si oui : verifier `.env` :
     - `UNIPILE_DSN` (avec scheme https://)
     - `UNIPILE_API_KEY`
     - **Un `account_id` PAR provider connecte** (1 par OAuth Unipile) :
       - `UNIPILE_LINKEDIN_ACCOUNT_ID` si LinkedIn
       - `UNIPILE_OUTLOOK_ACCOUNT_ID` si Outlook (Microsoft 365)
       - `UNIPILE_GMAIL_ACCOUNT_ID` si Gmail
     - Tester la connexion sur chaque provider configure
   - Si non : "Pas de souci, les commandes LinkedIn/email seront desactivees. Tu pourras les activer plus tard."

⚠️ **Piege classique** : un compte Unipile != un account_id. Unipile cree un
account_id par provider OAuth. Si l'utilisateur a connecte LinkedIn ET Outlook,
il a 2 account_id distincts a remplir dans 2 variables differentes.

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

Duree totale typique : ~15-20 min selon les pointeurs fournis a l'etape 0.

---

## Regles

1. **Etape par etape** — JAMAIS tout d'un coup, toujours attendre la reponse
2. **Idempotent** — relancer `/system init` ne doit pas casser ce qui est deja configure (demander avant d'ecraser)
3. **Pas d'invention** — si un outil ne marche pas, dire "ca marche pas" et aider a corriger. Si l'etape 0 deduit quelque chose, le presenter comme un brouillon a valider, jamais comme un fait.
4. **Validation humaine** — montrer le resultat de chaque etape, attendre "ok" avant de continuer
5. **WebFetch uniquement** — pour scraper LinkedIn ou un site, utiliser `WebFetch` (outil natif Claude Code). Pas de scraper Python custom, pas de service tiers.
