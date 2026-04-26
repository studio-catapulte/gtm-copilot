# Guides opérateur

Ces guides s'adressent à **l'opérateur du copilote** — la personne qui setup les comptes Unipile (génération de hosted auth links, configuration des scopes, récupération d'`account_id`, etc.).

Selon le contexte, l'opérateur peut être :

- **Le fondateur lui-même**, qui installe le copilote pour son propre usage. Dans ce cas, opérateur et utilisateur final sont la même personne.
- **Un tiers délégué** (agence, consultant, revendeur) qui setup pour un fondateur final. Le fondateur n'a alors qu'à cliquer un lien et valider un écran OAuth, pendant que l'opérateur s'occupe du reste.

Chaque guide est conçu pour être exécuté **une fois par compte à connecter** au moment de l'onboarding.

## Guides disponibles

- [`unipile-outlook.md`](./unipile-outlook.md) — connexion Outlook (Microsoft 365) via OAuth Microsoft, scopes mail + calendrier.
- `unipile-gmail.md` *(à venir)* — connexion Gmail via OAuth Google, équivalent du guide Outlook.
- `unipile-linkedin.md` *(à venir)* — connexion LinkedIn via Unipile (cookie ou hosted auth link).

## Lien avec le setup fondateur

Le guide quickstart côté fondateur est dans [`../SETUP.md`](../SETUP.md). Il référence ces guides opérateur quand une étape demande l'intervention de l'opérateur (génération de lien, récupération d'`account_id`, etc.). Si tu es à la fois fondateur et opérateur, tu enchaîneras simplement les deux côtés.
