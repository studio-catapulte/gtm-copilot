# Adapter email — ms365-mcp

Mappe le port `_shared/email.md` sur le **serveur MCP `@softeria/ms-365-mcp-server`**
(Microsoft Graph : Outlook Mail + Calendar). Provider pour un ecosysteme Microsoft 365.

## Nature : adapter MCP (pas de script, pas de venv)

Contrairement aux adapters CLI/Python, celui-ci est un **serveur MCP externe** a
declarer dans Claude Code. Les operations sont des **tool calls** `mcp__ms365__…`,
pas des commandes shell.

## Install (onboarding heterogene)

Ajouter le serveur MCP a la config Claude Code, ex :

```jsonc
// .mcp.json / config MCP
{
  "mcpServers": {
    "ms365": {
      "command": "npx",
      "args": ["-y", "@softeria/ms-365-mcp-server", "--preset", "mail,calendar", "--read-only"]
    }
  }
}
```

- Preset `mail,calendar` pour limiter la surface (le serveur expose 90+ tools sinon).
- `--read-only` tant qu'on ne veut pas d'ecriture.
- **Auth** : appeler le tool `login` (device code), confirmer avec `verify-login`.
- Multi-compte : passer `"account": "user@boite.com"` dans chaque tool call.
- `npx @softeria/ms-365-mcp-server --list-presets` / `--list-permissions` pour explorer.

## Mapping des operations

Noms de tools reels (1-to-1 avec Graph ; voir `--list-presets` / `endpoints.json`) :

| Operation | Tool MCP |
|-----------|----------|
| `list-inbox(unread)` | `list-mail-messages` (filtre `isRead eq false`) |
| `search(query)` | `list-mail-messages` (param `$search`) |
| `get(id)` | `get-mail-message` |
| `send(...)` | `send-mail` |
| `list-events(from,to)` | `list-calendar-events` (preset `calendar`) |
| `create-event(...)` | `create-calendar-event` |

> Les noms exacts des tools calendrier dependent de la version du serveur :
> verifier via `--list-presets`/`endpoints.json` avant de les cabler en dur.
