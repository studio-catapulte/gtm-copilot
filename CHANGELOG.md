# Changelog

Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/).

## [0.5.0] — 2026-07-01

Refonte de l'architecture en **skills-outils** (validée par un challenge de 3 revues
indépendantes). Fin du dossier `_shared` : chaque capacité est un skill à part entière
qui encapsule son outil, et les routines les référencent par chemin.

### Ajouté
- **Skills-outils `crm/`, `email/`, `meeting-notes/`** : chaque `SKILL.md` porte le
  **contrat** (opérations + schéma, SSOT qui protège les routines), et un sous-dossier
  `adapters/` contient le how-to par outil.
- **Mapping d'opérations Notion (REST)** dans `crm/adapters/notion.md` — comble un trou
  de v0.4 (aucune opération runtime n'était spécifiée). Adapter headless-safe.
- **Section `Outils actifs` dans `CLAUDE.md`** : le choix d'outil par capacité (le
  binding), lu par l'agent. Support **multi-compte** (ex. deux boîtes mail).

### Modifié
- **`_shared/{crm,email}.md` + `_shared/providers/` → `skills/{crm,email}/` + `adapters/`.**
  Le dossier `_shared` disparaît.
- **`fathom/` → `meeting-notes/`** : nommé par capacité ; Fathom devient un adapter
  (`adapters/fathom/`). Contrat lecture-seule (resolve/transcript/summary/action-items).
- **Le binding quitte `.env`** : plus de `CRM_PROVIDER`/`EMAIL_PROVIDER`. `.env` = secrets
  uniquement ; le choix d'outil vit dans `CLAUDE.md > Outils actifs`.
- Routines (`daily`, `weekly`, `sourcing`, `prep-meeting`, `system/init-repo`) rebranchées
  sur les nouveaux chemins ; onboarding déclare l'outil dans CLAUDE.md.
- **Recherche web** : pas de skill dédié (firecrawl déjà le défaut) — juste une ligne
  dans `CLAUDE.md > Outils actifs`.

## [0.4.0] — 2026-07-01

Le système devient **générique face au provider** via un modèle **ports & adapters** :
les skills parlent en capacités (CRM, email, LinkedIn), le choix de l'outil se fait
une fois dans `.env`, et ajouter un outil = écrire un seul fichier adapter.

### Ajouté
- **Port email + calendrier** (`_shared/email.md`) avec adapters interchangeables :
  `gmail-gog` (CLI Google), `ms365-mcp` (serveur MCP Microsoft 365), `unipile-outlook`
  (legacy). Un seul provider couvre mail + agenda.
- **Vocabulaire ports & adapters** documenté (README, CLAUDE.md) : port = contrat d'une
  capacité, adapter = connecteur vers un outil concret (CLI / script / MCP).
- Binding par `.env` : `EMAIL_PROVIDER`, et `CRM_PROVIDER` (renommé, voir Modifié).

### Modifié
- **Skill `unipile` → `linkedin`** : nommé par la capacité, pas le provider. Unipile
  devient l'**adapter unique** collé au skill. L'email/calendrier **quitte** Unipile.
- **CRM refondu en port + adapters** : `_shared/crm.md` = port ; `docs/crm/*` →
  `_shared/providers/crm/` (adapters exemples). Les CRM nommés (HubSpot, Attio, Folks…)
  sont **mentionnés** dans le README, pas fournis — un adapter = 1 fichier, liste ouverte.
- **Skills découplés de tout provider en dur** : `prep-meeting`, `weekly`, `daily` ne
  parlent plus de « CRM Notion » ni d'« Outlook Unipile » mais des ports `crm.md`/`email.md`.
- `CRM_TYPE` → **`CRM_PROVIDER`** (cohérence `*_PROVIDER`).
- `/system init-repo` : choix du provider email + **onboarding hétérogène** (setup adapté
  à la nature de chaque adapter : CLI, MCP, ou venv).

## [0.3.0] — 2026-07-01

Remise au niveau du terrain (backport du battle-testé en delivery). L'architecture
passe des `plugins/` + `tools/` éclatés à des **skills autoportants** : chaque
intégration embarque ses scripts Python et ses workflows d'invocation.

### Ajouté
- **Skill `fathom`** — transcripts, summaries et action items de meetings via l'API
  REST Fathom (script + workflow + setup venv). Câblé optionnellement dans
  `prep-meeting` pour les RDV de suivi.
- **`done` logue dans la daily** — append d'un bloc session à `logs/daily/YYYY-MM-DD.md`
  (Accompli / Décisions / Métriques / Pickup).
- **`weekly` réécrit `STATUS.md`** — snapshot macro vivant (pipeline + focus S+1),
  réécrit chaque semaine, jamais accumulé. `weekly` est le seul writer.
- `_shared/crm.md` — contrat CRM-agnostique comme référence transverse.

### Modifié
- **`unipile` est désormais un skill autoportant** (`.claude/skills/linkedin/`) :
  scripts Python + workflows + `SKILL.md`. Fin des dossiers `plugins/` et `tools/`.
- **`init` → `init-repo`** (sous l'umbrella `system`) pour éviter la collision avec
  le `/init` natif de Claude Code. Setup venv Fathom ajouté à l'onboarding.
- **Robustesse (backport générique kit-vincent)** : `prep-meeting` (guard contact
  absent du CRM, sources optionnelles, anti-invention), `daily` (tolérance aux
  pannes runtime), `sourcing` (guard ICP vide, over-fetch ~1.5x contre l'attrition
  du filtre).
- Auto-chargement du `.env` (last-wins) + `location`/`industry` en array.

### Supprimé
- **Skill `slides`** — un générique meilleur existe ailleurs.

## [0.1.0] — 2026-04-27

Version initiale gelée : skills `daily`, `weekly`, `sourcing`, `prep-meeting`,
`slides`, `system`, intégration Unipile en `plugins/` + `tools/`.
