---
name: daily
description: |
  Routine quotidienne de prospection commerciale. Check inbox (mail + LinkedIn),
  traite les nouvelles connexions, fait les relances, ajoute des prospects au pipe.
  ~30-40 minutes chaque matin.

  Triggers: /daily, "routine du matin", "prospection du jour", "quoi de neuf",
  "bonjour", debut de session.

  Utilise les outils : Unipile Outlook (tools/unipile/outlook.md),
  Unipile LinkedIn (tools/unipile/linkedin.md),
  Unipile Messaging (tools/unipile/messaging.md),
  CRM (tools/crm.md).
---

# /daily — Routine quotidienne

Chaque matin, meme process. L'objectif c'est d'avoir fait toutes ses actions
commerciales en 30-40 minutes, puis passer a autre chose.

## Etape 0 — Briefing (2 min)

Scanner le CRM et poser le contexte de la journee.

1. Lire `CLAUDE.md` pour rappeler le pipeline et les regles
2. Noter la date du jour et le jour de la semaine
3. **Snapshot pipeline** : compter les contacts par statut
4. **Follow-ups dus** : contacts avec `Next <= aujourd'hui`
5. **Meetings a venir** : contacts au statut "RDV pris" ou equivalent

Afficher :

```
Bonjour [Prenom] :)

[Jour, Date]

## Pipeline
- [Statut 1] : X | [Statut 2] : X | [Statut 3] : X
- Total actif : X contacts

## Aujourd'hui
- X follow-ups en retard
- X meetings a preparer
- [Suggestion contextuelle]

On attaque ?
```

**Suggestions contextuelles :**
- **Lundi** : "Nouvelle semaine, on planifie les actions"
- **Jour de bilan** (voir CLAUDE.md) : "C'est ton jour de bilan, on fait le `/weekly` apres la routine ?"
- **Pipeline vide (< 5 actifs)** : "Le pipe est light, on va forcer sur les invitations aujourd'hui"
- **Follow-ups > 3 jours de retard** : "X contacts oublies depuis plus de 3 jours"

**ATTENDRE** que l'utilisateur confirme avant de continuer.

---

## Etape 1 — Check inbox (5-10 min)

### 1a. Mails Outlook (si Pack Pro)

Suivre les instructions dans `tools/unipile/outlook.md` :

```bash
cd plugins/unipile && source venv/bin/activate
python outlook_client.py --user <nom> emails-list --folder INBOX --unread-only --limit 50
```

Classer chaque mail non-lu :

| Categorie | Action |
|---|---|
| **Reponse prospect** | Lire le detail, matcher avec le CRM, proposer un draft |
| **Admin / ops** | Resume en 1 ligne |
| **Notif / newsletter / spam** | Compter, ignorer |

Pour chaque reponse prospect :
1. Lire le mail complet (`email-get <EMAIL_ID>`)
2. Chercher l'expediteur dans le CRM
3. Proposer un draft de reponse (style de `knowledge/tone-of-voice.md`)
4. Si proposition de RDV : checker la dispo d'abord (`availability`)
5. **Montrer le draft, attendre validation avant envoi**

### 1b. Messages LinkedIn

```bash
python plugins/unipile/messaging_client.py chats --provider LINKEDIN --limit 20
```

Identifier les messages non lus, lire le contenu :

```bash
python plugins/unipile/messaging_client.py messages CHAT_ID --limit 10
```

Cross-referencer avec le CRM. Proposer une reponse pour chaque message recu
(objectif = decrocher un RDV). **Montrer chaque message pour validation.**

### Output etape 1

```
## Inbox
- Mails : X non-lus (Y prospects, Z admin, W ignores)
- LinkedIn : X conversations actives

### Reponses prospects
1. [Nom] ([Entreprise]) — [canal] — [resume]
   Draft : [message propose]
   → Envoyer ? (oui / modifier / passer)
```

---

## Etape 2 — Nouvelles connexions LinkedIn (5 min)

Recuperer les connexions recentes :

```python
import sys; sys.path.insert(0, 'plugins/unipile')
from linkedin_client import UnipileLinkedInClient
client = UnipileLinkedInClient()
contacts = client.get_contacts(limit=50)
```

Cross-referencer avec le CRM (contacts au statut "Invitation" ou equivalent).
**Normaliser les noms** (accents, casse) avant de comparer.

Pour chaque nouvelle acceptation :
1. Lire `knowledge/tone-of-voice.md` pour le style
2. Rediger un premier message personnalise (setting message)
3. **Montrer pour validation**
4. Envoyer via `tools/unipile/messaging.md` (guillemets simples obligatoires)
5. Mettre a jour le CRM : statut → "Connecte", Dernier contact = aujourd'hui

### Output etape 2

```
## Nouvelles connexions
X nouvelles acceptations :
1. [Nom] ([Entreprise]) — message propose : "..."
   → Envoyer ? (oui / modifier / passer)
```

---

## Etape 3 — Relances (10 min)

Query le CRM : `Next <= aujourd'hui` ET statut dans les etapes actives du pipeline.
Trier par date Next ascendante (les plus en retard d'abord).

Pour chaque contact :
1. Lire les Notes CRM pour le contexte
2. Determiner le canal (LinkedIn si connecte, email sinon)
3. Rediger un message de relance :
   - Court (3-5 lignes max)
   - Dans le ton du fondateur (`knowledge/tone-of-voice.md`)
   - Reference au dernier echange
   - Finit par une question ou une proposition concrete
   - **Pas de tirets cadratins**, accents obligatoires
4. **Montrer pour validation**
5. Envoyer via le canal appropriate (`tools/unipile/messaging.md` ou `tools/unipile/outlook.md`)
6. Mettre a jour le CRM : Dernier contact, Next, Notes

Si un contact a atteint le max de follow-ups (voir CLAUDE.md) → proposer "Perdu" ou "Nurturing".

### Output etape 3

```
## Relances
X contacts a relancer :
1. [Nom] ([Entreprise]) — [canal] — dernier contact il y a X jours
   Message : "..."
   → Envoyer ? (oui / modifier / passer)
```

---

## Etape 4 — Invitations LinkedIn (5-10 min)

Remplir le pipe avec de nouveaux prospects.

1. Query CRM : contacts au statut "Pool", limit 20
2. Pour chaque contact :
   - Verifier qu'on a un LinkedIn profile ID ou URL
   - Verifier si on est DEJA connecte : `client.get_profile(slug)` → `network_distance`
     - Si FIRST_DEGREE → passer a "Connecte" + envoyer un message (etape 2 logic)
     - Sinon → invitation **SANS note** (meilleur taux d'acceptation)
3. Montrer la liste pour validation groupee
4. Envoyer les invitations via `tools/unipile/linkedin.md`
5. Mettre a jour le CRM : statut → "Invitation", Dernier contact = aujourd'hui

### Limites LinkedIn

- **Max 20 invitations/jour**, ~100/semaine
- Respecter un delai de quelques secondes entre chaque action
- **TOUJOURS demander confirmation avant d'envoyer**

### Output etape 4

```
## Invitations
X invitations a envoyer :
1. [Nom] ([Entreprise]) — [titre]
2. [Nom] ([Entreprise]) — [titre]
...

Envoyer les X invitations ? (oui / modifier la liste / annuler)
```

---

## Etape 5 — Resume (1 min)

```
## Routine terminee — X minutes

| Action | Nombre |
|--------|--------|
| Mails prospects traites | X |
| Messages LinkedIn traites | X |
| Setting messages envoyes | X |
| Relances envoyees | X |
| Invitations envoyees | X/20 |

Prochaines actions :
- [contacts avec Next demain]
- [meetings a preparer]
- Quota invitations restant cette semaine : X
```

---

## Regles

1. **JAMAIS envoyer sans validation** du fondateur — chaque message est montre avant envoi
2. **Etape par etape** — finir une etape avant de passer a la suivante
3. **CRM = source de verite** — toujours lire avant d'agir, toujours mettre a jour apres
4. **Pas de triage automatique en tache de fond** — c'est une routine humaine assistee
5. Si le fondateur est presse : proposer de skip les etapes non-critiques

## Si pas de Pack Pro

Sans Unipile, les etapes 1b, 2, 4 sont desactivees. La routine se reduit a :
- Etape 0 : briefing CRM
- Etape 3 : relances (messages a copier-coller manuellement)

Le fondateur peut quand meme utiliser `/prep-meeting` et `/bilan` normalement.
