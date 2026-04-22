# GTM Copilot

Ton copilote connait ton business (`knowledge/`), sait vendre pour toi (`skills`), et se branche sur tes outils (CRM, email, LinkedIn) en coulisses. Parle-lui en francais. Il ne fait rien sans ton accord.

## Commandes

| Dis ca | Ce qui se passe | Frequence |
|--------|----------------|-----------|
| "Routine du matin" | Check inbox + nouvelles connexions + relances + invitations LinkedIn | Quotidien |
| "Weekly" | Review : wins, pipeline, objectifs semaine prochaine | Hebdo |
| "Prepare mon RDV avec X" | Profil LinkedIn + entreprise + questions suggerees | A la demande |
| "Trouve-moi des prospects" | Recherche LinkedIn + qualification + ajout CRM | A la demande |
| "Fais des slides pour X" | Presentation HTML personnalisee pour un prospect | A la demande |

## Setup

### 1. Installer Claude Code

Telecharger [Claude Code](https://claude.ai) (app desktop ou terminal). Abonnement Claude Pro (20 EUR/mois).

### 2. Configurer le CRM

C'est la premiere chose a faire. Le CRM est la source de verite de tout le systeme.

1. Creer un compte [Airtable](https://airtable.com) (gratuit)
2. Suivre le guide complet dans `tools/crm.md` (creation de la base, des champs, import contacts)
3. Generer un API token sur airtable.com/create/tokens
4. Copier `.env.example` en `.env` et remplir les variables Airtable

```bash
cp .env.example .env
# Editer .env avec vos cles
```

> Autre CRM ? Notion, NocoDB, HubSpot, Pipedrive sont aussi supportes. Voir `tools/crm.md`.

### 3. Personnaliser

1. Ouvrir `CLAUDE.md` et remplacer tous les `[PLACEHOLDERS]` avec vos infos
2. Remplir les fichiers dans `knowledge/` :
   - `pitch.md` — votre offre et differenciateurs
   - `icp.md` — profil client ideal
   - `objections.md` — objections frequentes + reponses
   - `tone-of-voice.md` — exemples de messages dans votre style

### 4. Connecter email + LinkedIn

Connecter Outlook et LinkedIn via Unipile :
- Voir `SETUP-UNIPILE-OUTLOOK.md` pour la procedure OAuth
- Ajouter `UNIPILE_DSN` et `UNIPILE_API_KEY` dans `.env`

### 5. Lancer

Ouvrir Claude Code dans ce dossier et dire "Routine du matin".

## Structure du repo

```
knowledge/          Ce que le copilote sait sur ton business
.claude/skills/     Ce que le copilote sait faire (5 commandes)
tools/              Plomberie interne (APIs, CRM) — tu n'y touches pas
plugins/            Code Python pour les appels API — tu n'y touches pas
```

## Support

Nefia — contact@nefia.fr
