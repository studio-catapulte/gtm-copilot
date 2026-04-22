---
name: system
description: |
  Maintenance du copilote : setup initial et cloture de session.
  Utilise ce skill quand l'utilisateur veut : (1) configurer le copilote pour
  la premiere fois, (2) cloturer sa session de travail, (3) dire "fin de session",
  "on s'arrete la", "wrap up", "premiere fois", "on demarre", "initialise le repo".
  Triggers: /system, /system init, /done, /system done.
---

# /system — Maintenance du copilote

Skill de maintenance du repo et du copilote. Deux workflows :

## Routing

| Trigger | Workflow |
|---------|----------|
| `/system` ou `/system init` ou "premiere fois" | → Lire `workflows/init.md` |
| `/done` ou `/system done` ou "fin de session" | → Lire `workflows/done.md` |

Si l'utilisateur tape `/system` sans precision et que le repo est deja configure
(CLAUDE.md ne contient plus de `[PLACEHOLDER]`), demander :
"Tu veux cloturer ta session (`/done`) ?"
