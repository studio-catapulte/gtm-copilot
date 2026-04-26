# Guides opérateur (Nefia)

Ces guides s'adressent à **Nefia, l'opérateur du copilote**, pas au fondateur client. Ils couvrent les manipulations techniques que Nefia exécute lors de l'onboarding d'un nouveau client (génération de liens OAuth, configuration des scopes, récupération d'`account_id`, etc.).

Chaque guide est conçu pour être exécuté **une fois par client** au moment de l'onboarding. Le fondateur client n'a généralement qu'à cliquer un lien et valider un écran OAuth.

## Guides disponibles

- [`unipile-outlook.md`](./unipile-outlook.md) — connexion Outlook (Microsoft 365) via OAuth Microsoft, scopes mail + calendrier.
- `unipile-gmail.md` *(à venir)* — connexion Gmail via OAuth Google, équivalent du guide Outlook.
- `unipile-linkedin.md` *(à venir)* — connexion LinkedIn via Unipile (cookie ou hosted auth link).

## Lien avec le setup fondateur

Le guide quickstart côté fondateur est dans [`../SETUP.md`](../SETUP.md). Il référence ces guides opérateur quand une étape demande l'intervention de Nefia (génération de lien, récupération d'`account_id`, etc.).
