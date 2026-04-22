---
name: slides
description: |
  [PACK PRO] Cree des presentations HTML personnalisees pour un prospect.
  Duplique un template, adapte le contenu, exporte en PDF si besoin.

  Triggers: "fais des slides pour [Nom]", "cree une presentation",
  "slides pour le RDV avec [Nom]".
---

# Slides — Presentation personnalisee

Genere une presentation HTML personnalisee pour un prospect.

## Process

### 1. Brief rapide

Si l'input est incomplet, demander en UNE question :

```
Pour la presentation, j'ai besoin de :
1. **Prospect** : Nom, entreprise, role (ou lien LinkedIn/CRM)
2. **Type** : Discovery / Proposition commerciale / Demo
3. **Longueur** : Court (5-8 slides) / Moyen (8-14) / Long (14+)
```

### 2. Enrichir le prospect

**AVANT de generer**, collecter les donnees du prospect :
- CRM Notion : fiche existante, notes, historique
- Web search : site entreprise, actualites
- Si Pack Pro : profil LinkedIn via Unipile

Extraire : nom entreprise, taille, secteur, localisation, enjeux identifies.

### 3. Generer

1. **Copier** le template depuis `templates/slides-template.html`
2. **Structure recommandee** :
   - Slides 1-4 : le prospect (son contexte, ses douleurs, son marche) — c'est le plus important
   - Slide 5 : la transition ("et si...")
   - Slides 6-8 : la solution (notre offre, comment ca marche)
   - Slide 9 : les benefices chiffres (avant/apres)
   - Slide 10 : le pricing ou le next step
3. **Remplacer** tous les `{{...}}` avec les donnees enrichies
4. **Verifier** : accents francais, pas d'emojis (Lucide icons si besoin)

Nommage : `[type]-[prospect].html` (ex: `discovery-dupont.html`)
Ecrire dans le dossier racine du repo.

### 4. Export PDF (optionnel)

Si l'utilisateur veut un PDF :
```bash
# Ouvrir dans le navigateur et imprimer en PDF
open [fichier].html
```

Ou si Playwright est disponible :
```bash
npx playwright screenshot [fichier].html [fichier].pdf --full-page
```

## Regles

- **Le prospect d'abord** (slides 1-4), l'offre apres (slide 5+)
- HTML vanilla, pas de framework
- Ne pas sur-variabiliser le template (garder simple)
- Parler du prospect, pas de nous
