---
name: sourcing
description: |
  Recherche de nouveaux leads sur LinkedIn. Cherche, qualifie vs ICP,
  deduplique avec le CRM, ajoute au pipeline en statut "Pool".
  A utiliser quand le pipeline est vide ou qu'on veut attaquer un nouveau segment.

  Triggers: /sourcing, "trouve-moi des prospects", "cherche des leads",
  "remplis le pipeline", "sourcing".

  Utilise les outils : LinkedIn (tools/unipile/linkedin.md),
  Enrichissement (tools/enrichment.md), CRM (tools/crm.md).
---

# /sourcing — Recherche de nouveaux leads

Trouver de nouveaux prospects qualifies et les ajouter au CRM.

## Process

### Etape 1 — Criteres de recherche

Demander les criteres (ou les deduire du contexte) :
- Titre du decideur
- Secteur / industrie
- Localisation
- Taille entreprise
- Mots-cles specifiques

Verifier que les criteres matchent le ICP (`knowledge/icp.md`).
Si les criteres divergent du ICP, le signaler.

### Etape 2 — Recherche LinkedIn

Suivre les instructions dans `tools/unipile/linkedin.md` :

```python
import sys; sys.path.insert(0, 'plugins/unipile')
from linkedin_client import UnipileLinkedInClient
client = UnipileLinkedInClient()
results = client.search_people(keywords="...", location="...", title="...")
```

### Etape 3 — Qualification + deduplication

Pour chaque resultat :
1. **Deduplication** : chercher dans le CRM par LinkedIn URL ou nom+entreprise
2. **Qualification vs ICP** : noter sur 3 criteres (titre, taille, secteur)
3. **Enrichir si besoin** : `client.get_profile(slug)` pour le profil complet

Presenter les resultats :

```
## Resultats recherche

X profils trouves, Y qualifies, Z deja dans le CRM.

| # | Nom | Entreprise | Titre | Localisation | Score ICP |
|---|-----|-----------|-------|-------------|-----------|
| 1 | [Nom] | [Entreprise] | [Titre] | [Ville] | ★★★ |
| 2 | [Nom] | [Entreprise] | [Titre] | [Ville] | ★★☆ |

Ajouter au CRM ? (tous / selectionner / annuler)
```

**ATTENDRE la validation.**

### Etape 4 — Ajout au CRM

Pour chaque lead valide :
- Creer un contact dans le CRM en statut "Pool"
- Remplir : Nom, Entreprise, LinkedIn URL, Source = "LinkedIn Search"
- Notes : "[date] — sourced via LinkedIn, criteres : [criteres]"

### Etape 5 — Enrichissement (optionnel)

Proposer :
```
Tu veux enrichir ces leads (email + telephone via FullEnrich) ?
Consomme 1 credit par contact trouve. X contacts = max X credits.
1. Oui, tous
2. Oui, seulement les ★★★
3. Non, on fera plus tard
```

Si oui, suivre `tools/enrichment.md` pour chaque contact.

## Output

```
## Sourcing termine

- X leads ajoutes au CRM en statut "Pool"
- Y enrichis (email/tel)
- Prochaine etape : ils seront invites lors de la prochaine /daily (etape 4)
```

## Regles

- **Toujours verifier les doublons** avant d'ajouter au CRM
- **Toujours inclure le profil LinkedIn**
- Qualifier avant d'ajouter — pas de leads hors ICP dans le pipe
