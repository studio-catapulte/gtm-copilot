# Changelog

Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/).

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
