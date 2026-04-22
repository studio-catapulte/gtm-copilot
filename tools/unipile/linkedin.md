# Unipile LinkedIn — Recherche et enrichissement

Wrapper technique pour la recherche de profils, l'enrichissement, et les invitations LinkedIn via l'API Unipile.
Ce fichier est une reference interne, appelee par les skills `/prospection` et `/prep-meeting`.

## Prerequis

- `UNIPILE_DSN` et `UNIPILE_API_KEY` dans `.env`
- Venv Python : `plugins/unipile/venv`
- Compte LinkedIn connecte dans Unipile

## Recherche de profils

```python
import sys; sys.path.insert(0, 'plugins/unipile')
from linkedin_client import UnipileLinkedInClient
client = UnipileLinkedInClient()

# Recherche par criteres
results = client.search_people(keywords="directeur", location="Lyon", title="DG")

# Profil complet
profile = client.get_profile('SLUG')
import json; print(json.dumps(profile, indent=2, default=str))

# Contacts recents (connexions)
contacts = client.get_contacts(limit=50)
```

## Donnees extraites d'un profil

- Nom complet, titre actuel, entreprise
- Localisation
- Experience (postes precedents pertinents)
- Formation
- Nombre de connexions
- `network_distance` (FIRST_DEGREE = deja connecte)
- Provider ID (ACoAA...) pour Unipile messaging

## Envoi d'invitations

```bash
python plugins/unipile/messaging_client.py invite PROVIDER_ID
```

- **Max 20 invitations/jour**, ~100/semaine
- Invitations **SANS note** par defaut (meilleur taux d'acceptation)
- Les invitations avec note sont limitees a 300 caracteres
- Respecter un delai de quelques secondes entre chaque action
- **TOUJOURS demander confirmation avant d'envoyer**

## Regles

- Jamais d'action automatique sans validation du fondateur
- Normaliser les noms (accents, casse) avant comparaison CRM
