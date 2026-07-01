#!/usr/bin/env python3
"""
Fathom REST API client — transcripts, summaries, action items.

Pas de MCP officiel Fathom au 03-06-2026. On parle directement à l'API REST
documentée sur https://docs.fathom.video/.

Usage CLI :
    python fathom_client.py meetings --limit 10
    python fathom_client.py summary <recording_id>
    python fathom_client.py transcript <recording_id>
    python fathom_client.py resolve <call_id_or_url>   # call_id ou URL → recording_id

Usage module :
    from fathom_client import FathomClient
    client = FathomClient()
    meetings = client.list_meetings(include_summary=True)
    transcript = client.get_transcript(recording_id)

Config : FATHOM_API_KEY dans `.env` à la racine du kit (chargée via python-dotenv
ou sourcée par le shell parent).
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

API_BASE = "https://api.fathom.ai/external/v1"


def find_kit_root(start_path: Optional[Path] = None) -> Path:
    """Remonte vers la racine du kit (présence de CLAUDE.md ou settings.local.json)."""
    if start_path is None:
        start_path = Path(__file__).parent
    current = start_path.resolve()
    while current != current.parent:
        if (current / "CLAUDE.md").is_file() or (current / "settings.local.json").is_file():
            return current
        current = current.parent
    return Path(__file__).parent.parent.parent


def _load_dotenv(env_path: Path) -> None:
    """Mini parser .env sans dépendance — KEY=VALUE par ligne, # = commentaire."""
    if not env_path.is_file():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def get_api_key() -> str:
    if "FATHOM_API_KEY" not in os.environ:
        _load_dotenv(find_kit_root() / ".env")
    api_key = os.environ.get("FATHOM_API_KEY")
    if not api_key:
        raise RuntimeError(
            "FATHOM_API_KEY introuvable. Renseigne-la dans `.env` à la racine du "
            "kit (`FATHOM_API_KEY=...`) ou exporte-la dans le shell."
        )
    return api_key


class FathomClient:
    def __init__(self, api_key: Optional[str] = None, base: str = API_BASE):
        self.api_key = api_key or get_api_key()
        self.base = base.rstrip("/")
        self._session = requests.Session()
        self._session.headers.update({"X-Api-Key": self.api_key})

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base}{path}"
        resp = self._session.get(url, params=params or {}, timeout=30)
        if resp.status_code == 401:
            raise RuntimeError("Fathom API: 401 Unauthorized — vérifie FATHOM_API_KEY.")
        if resp.status_code == 404:
            raise RuntimeError(f"Fathom API: 404 sur {path} (ressource introuvable ou accès refusé).")
        resp.raise_for_status()
        return resp.json()

    def list_meetings(
        self,
        include_summary: bool = False,
        include_transcript: bool = False,
        include_action_items: bool = False,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {}
        if include_summary:
            params["include_summary"] = "true"
        if include_transcript:
            params["include_transcript"] = "true"
        if include_action_items:
            params["include_action_items"] = "true"
        data = self._get("/meetings", params=params)
        items = data if isinstance(data, list) else data.get("items") or data.get("meetings") or []
        if limit is not None:
            items = items[:limit]
        return items

    def get_summary(self, recording_id: str) -> Dict[str, Any]:
        return self._get(f"/recordings/{recording_id}/summary")

    def get_transcript(self, recording_id: str) -> Dict[str, Any]:
        return self._get(f"/recordings/{recording_id}/transcript")

    def get_recording_by_call_id(self, call_id: str) -> Optional[Dict[str, Any]]:
        meetings = self.list_meetings()
        for m in meetings:
            url = m.get("url") or m.get("recording_url") or ""
            if f"/calls/{call_id}" in url:
                return m
        return None

    def resolve(self, identifier: str) -> Dict[str, Any]:
        """Résout un call_id, une URL /calls/<id>, ou un recording_id en metadata."""
        match = re.search(r"/calls/(\d+)", identifier)
        if match:
            call_id = match.group(1)
            found = self.get_recording_by_call_id(call_id)
            if found:
                return found
            raise RuntimeError(f"call_id {call_id} introuvable dans les meetings accessibles.")
        if identifier.isdigit():
            found = self.get_recording_by_call_id(identifier)
            if found:
                return found
        try:
            return self.get_summary(identifier)
        except RuntimeError:
            raise RuntimeError(
                f"Impossible de résoudre `{identifier}` (ni call_id, ni recording_id valide)."
            )


def _print_json(value: Any) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, default=str))


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Fathom REST API client")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_meetings = sub.add_parser("meetings", help="Liste les meetings accessibles")
    p_meetings.add_argument("--limit", type=int, default=None)
    p_meetings.add_argument("--with-summary", action="store_true")
    p_meetings.add_argument("--with-transcript", action="store_true")
    p_meetings.add_argument("--with-action-items", action="store_true")

    p_summary = sub.add_parser("summary", help="Summary d'un recording")
    p_summary.add_argument("recording_id")

    p_transcript = sub.add_parser("transcript", help="Transcript d'un recording")
    p_transcript.add_argument("recording_id")

    p_resolve = sub.add_parser("resolve", help="Résout call_id ou URL /calls/<id>")
    p_resolve.add_argument("identifier")

    args = parser.parse_args(argv)
    client = FathomClient()

    if args.cmd == "meetings":
        _print_json(
            client.list_meetings(
                include_summary=args.with_summary,
                include_transcript=args.with_transcript,
                include_action_items=args.with_action_items,
                limit=args.limit,
            )
        )
    elif args.cmd == "summary":
        _print_json(client.get_summary(args.recording_id))
    elif args.cmd == "transcript":
        _print_json(client.get_transcript(args.recording_id))
    elif args.cmd == "resolve":
        _print_json(client.resolve(args.identifier))
    else:
        parser.print_help()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
