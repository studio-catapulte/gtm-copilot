# Unipile Messaging — Envoi de messages multi-canal

Wrapper technique pour envoyer et lire des messages LinkedIn, WhatsApp, Instagram via l'API Unipile.
Ce fichier est une reference interne, appelee par les skills `/prospection` et `/relances`.

## Prerequis

- `UNIPILE_DSN` et `UNIPILE_API_KEY` dans `.env`
- Venv Python : `plugins/unipile/venv`
- Compte LinkedIn connecte dans Unipile

## Lister les conversations recentes

```bash
cd plugins/unipile && source venv/bin/activate
python messaging_client.py chats --provider LINKEDIN --limit 20
```

## Lire les messages d'une conversation

```bash
python messaging_client.py messages CHAT_ID --limit 10
```

> Si le CHAT_ID commence par `-`, prefixer avec `--` : `messages -- -CHAT_ID`

## Envoyer un message

### A un contact avec conversation existante (dans les 50 recentes)

```bash
python messaging_client.py send CHAT_ID --text 'Votre message ici'
```

### A un contact SANS conversation recente

Utiliser `new-chat` avec le Provider ID du contact (ACoAA...) :

```bash
python messaging_client.py new-chat --attendee-id PROVIDER_ID --text 'Votre message ici'
```

Cela reutilise la conversation existante si elle existe, ou en cree une nouvelle.

## Regles critiques

1. **Guillemets simples obligatoires** pour le `--text` — les guillemets doubles ajoutent des backslashes dans le message
2. **Pas de tirets cadratins** dans les messages (utiliser des virgules)
3. **TOUJOURS demander confirmation** avant d'envoyer
4. **Accents francais obligatoires** dans tous les messages
5. Apres envoi, mettre a jour le CRM (Dernier contact, Next, Notes)
