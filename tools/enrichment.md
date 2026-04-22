# FullEnrich — Enrichissement email + telephone

Recupere l'email professionnel et/ou le telephone d'un contact a partir de son profil LinkedIn.
Ce fichier est une reference interne, appelee par le skill `/prospection`.

## Prerequis

- `FULLENRICH_API_KEY` dans `.env`
- Le profil LinkedIn du contact (URL ou slug)

## Process

### 1. Lancer l'enrichissement

```bash
curl -s -X POST "https://api.fullenrich.com/api/v1/contact/enrich" \
  -H "Authorization: Bearer $FULLENRICH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"linkedin_url": "https://www.linkedin.com/in/SLUG/"}'
```

### 2. Recuperer le resultat

L'enrichissement peut prendre 30-60 secondes :

```bash
curl -s "https://api.fullenrich.com/api/v1/contact/enrich/ENRICH_ID" \
  -H "Authorization: Bearer $FULLENRICH_API_KEY"
```

## Cout

- 1 credit par contact (uniquement si un resultat est trouve)
- **Toujours demander confirmation** avant de lancer : "Ca consomme 1 credit FullEnrich. On y va ?"

## Donnees retournees

- Email professionnel (si trouve)
- Telephone (si trouve)
- Taux de confiance

## Apres enrichissement

Mettre a jour le CRM :
- Email, Telephone (si trouves)
- Notes += "[date] — enrichi via FullEnrich"
