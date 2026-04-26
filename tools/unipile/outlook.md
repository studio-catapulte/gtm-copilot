# Unipile Outlook — Email + Calendar

Wrapper technique pour piloter les boites Outlook connectees via l'API Unipile.
Ce fichier est une reference interne, appelee par les skills `/inbox`, `/briefing`, `/prep-meeting`.

## Prerequis

- `plugins/unipile/unipile-config.json` contient `api_key`, `dsn`, et au moins
  une entree `services.unipile-outlook.<user>.account_id`
- Les comptes Outlook sont connectes dans Unipile (OAuth Microsoft via dashboard)
- **Scopes calendar actives** dans Dashboard Unipile -> Settings -> Microsoft OAuth
- Venv Python : `plugins/unipile/venv`

Si les comptes ne sont pas connectes, voir `docs/operators/unipile-outlook.md`.

## Invocation

Toutes les commandes passent par le client Python :

```bash
cd plugins/unipile && source venv/bin/activate
python outlook_client.py --user <nom> <sous-commande> [options]
```

Le `<nom>` est la clef definie dans `unipile-config.json` sous
`services.unipile-outlook.<nom>.account_id`.

## Sous-commandes

### Lecture email

```bash
# 10 derniers mails (tous dossiers)
python outlook_client.py --user <nom> emails-list --limit 10

# Non-lus de l'inbox
python outlook_client.py --user <nom> emails-list --folder INBOX --unread-only

# Recherche plein-texte
python outlook_client.py --user <nom> email-search --query "cabinet dupont"

# Detail d'un mail (body complet)
python outlook_client.py --user <nom> email-get <EMAIL_ID>

# Dossiers / labels
python outlook_client.py --user <nom> folders
```

### Envoi email

**Regle absolue : jamais d'envoi sans confirmation utilisateur explicite.**

Avant d'appeler `email-send`, afficher le draft complet (to, subject, body)
et demander "J'envoie ? (oui / non / modifier)". Attendre la reponse.

```bash
python outlook_client.py --user <nom> email-send \
  --to "prospect@ex.com" \
  --subject "Suite a notre echange" \
  --body "Bonjour ..."
```

Pour repondre dans un thread existant, passer `--reply-to <EMAIL_ID>`.

### Lecture calendrier

```bash
# Events de la semaine
python outlook_client.py --user <nom> events-list \
  --from 2026-04-10 --to 2026-04-17

# Events d'un calendrier specifique
python outlook_client.py --user <nom> events-list --calendar-id <ID>

# Lister les calendriers du compte
python outlook_client.py --user <nom> calendars-list
```

### Creer un event (RDV)

**Meme regle : confirmation explicite avant creation.**

```bash
python outlook_client.py --user <nom> event-create \
  --title "RDV discovery — <Nom Prospect>" \
  --start "2026-04-15T14:00:00" \
  --end   "2026-04-15T14:45:00" \
  --attendees "prospect@ex.com" \
  --description "Discovery call" \
  --location visio
```

- `--location visio` ajoute automatiquement un lien Teams.
- `--no-video` si pas besoin de visio.

### Check de dispo

```bash
python outlook_client.py --user <nom> availability \
  --from 2026-04-15T09:00 --to 2026-04-15T18:00
```

Retourne les creneaux **occupes**. Le caller croise avec les creneaux souhaites
pour proposer des slots libres.

## Erreurs courantes

- `Aucun account_id Outlook configure` → le compte n'est pas encore connecte. Voir `docs/operators/unipile-outlook.md`.
- `401 insufficient_privileges` sur calendar → les scopes calendar ne sont pas actives dans le Dashboard Unipile. Aller dans Settings -> Microsoft OAuth -> activer les 4 scopes `Calendars.*` -> reconnect le compte via hosted auth link.
- `401 API` sur email → `UNIPILE_API_KEY` expire ou mauvais DSN. Verifier `unipile-config.json`.
