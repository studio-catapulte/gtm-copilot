#!/usr/bin/env python3
"""
Unipile Outlook Client — Email + Calendar via l'API Unipile.

Wrap les endpoints /emails et /calendars pour les comptes Outlook (Microsoft 365)
connectes dans Unipile. Provider-agnostique cote code : marchera aussi pour
Gmail / IMAP une fois le bon account_id fourni.

Usage :
    # Config (une seule fois, voir unipile-config.json services.unipile-outlook)
    python outlook_client.py accounts                          # Lister comptes email/calendar

    # Email
    python outlook_client.py emails-list --limit 10
    python outlook_client.py emails-list --folder INBOX --limit 20 --unread-only
    python outlook_client.py email-get EMAIL_ID
    python outlook_client.py email-send --to bob@ex.com --subject "Hi" --body "Hello"
    python outlook_client.py email-send --to bob@ex.com --subject "Re" --body "..." --reply-to EMAIL_ID
    python outlook_client.py email-search --query "mot-cle"
    python outlook_client.py folders

    # Calendar
    python outlook_client.py calendars-list
    python outlook_client.py events-list --from 2026-04-10 --to 2026-04-17
    python outlook_client.py event-create --title "RDV Prospect X" \\
        --start "2026-04-15T14:00:00" --end "2026-04-15T14:45:00" \\
        --attendees "prospect@ex.com" --location "visio"
    python outlook_client.py event-delete EVENT_ID
    python outlook_client.py availability --from 2026-04-15T09:00 --to 2026-04-15T18:00

Options communes :
    --account-id ID    Override l'account_id par defaut (config)
    --user <nom>       Choisit le compte depuis services.unipile-outlook.<nom>

Notes :
- Les endpoints exacts sont bases sur la doc Unipile publique (2026-04).
- Certains endpoints calendar sont marques TO_VALIDATE — a tester au 1er run.
- Toujours confirmer cote utilisateur AVANT email-send et event-create.
"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, Optional, List

sys.path.insert(0, str(Path(__file__).parent))

from unipile_auth import api_request, api_request_paginated, get_service_config


SERVICE_NAME = "unipile-outlook"


def _to_iso_full(dt_str: str, end_of_day: bool = False) -> str:
    """
    Normalise une date/datetime en ISO 8601 complet avec ms (YYYY-MM-DDTHH:MM:SS.sssZ).
    Accepte: "2026-04-10", "2026-04-10T14:00", "2026-04-10T14:00:00", "...Z".
    """
    s = dt_str.strip()
    # Si date pure, ajouter T00:00:00 (ou T23:59:59 si end_of_day)
    if "T" not in s:
        s += "T23:59:59" if end_of_day else "T00:00:00"
    # Enlever Z final s'il y est, on le remet proprement
    if s.endswith("Z"):
        s = s[:-1]
    # Couper micro/nanosecondes eventuelles
    if "." in s:
        s = s.split(".")[0]
    return s + ".000Z"


class UnipileOutlookClient:
    """Client email + calendar via l'API Unipile (Outlook / Gmail / IMAP)."""

    def __init__(self, account_id: Optional[str] = None, user: Optional[str] = None):
        """
        Initialise le client.

        Args:
            account_id: Override direct de l'account_id (prioritaire).
            user: Nom de l'utilisateur dans la config (clef libre).
                  Cherche services.unipile-outlook.{user}.account_id.
        """
        config = get_service_config(SERVICE_NAME)
        resolved = None
        if account_id:
            resolved = account_id
        elif user and user in config:
            resolved = config[user].get("account_id")
        if not resolved:
            resolved = os.environ.get("UNIPILE_ACCOUNT_ID")
        if not resolved:
            # Fallback legacy : services.unipile-outlook.default_account_id
            resolved = config.get("default_account_id")
        self.default_account_id = resolved

    def _resolve_account_id(self, account_id: Optional[str] = None) -> str:
        acct = account_id or self.default_account_id
        if not acct:
            raise ValueError(
                "Aucun account_id Outlook configure. Voir unipile-config.json "
                "services.unipile-outlook.<user>.account_id"
            )
        return acct

    # ------------------------------------------------------------------ #
    # Generique
    # ------------------------------------------------------------------ #

    def list_accounts(self, limit: int = 50) -> Dict[str, Any]:
        """Liste tous les comptes Unipile (tous providers)."""
        return api_request_paginated("GET", "/api/v1/accounts", limit=limit)

    # ------------------------------------------------------------------ #
    # EMAILS
    # ------------------------------------------------------------------ #

    def list_emails(
        self,
        folder: Optional[str] = None,
        unread_only: bool = False,
        since: Optional[str] = None,
        limit: int = 20,
        cursor: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Liste les emails d'un compte.

        Args:
            folder: Nom du dossier (INBOX, SENT, DRAFTS, ...). Defaut : tout.
            unread_only: Ne retourne que les non-lus.
            since: Date ISO (2026-04-01) — emails recus apres.
            limit: Nb max de resultats.
            cursor: Pagination.
        """
        params: Dict[str, Any] = {"account_id": self._resolve_account_id(account_id)}
        # folder accepte soit un role Unipile (inbox/sent/drafts/trash/spam/archive),
        # soit un ID de dossier brut. On detecte par nom usuel.
        if folder:
            role_map = {
                "INBOX": "inbox", "SENT": "sent", "DRAFTS": "drafts",
                "TRASH": "trash", "SPAM": "spam", "ARCHIVE": "archive",
            }
            role = role_map.get(folder.upper())
            if role:
                params["role"] = role
            else:
                params["folder_id"] = folder  # ID brut
        if unread_only:
            if "role" not in params and "folder_id" not in params:
                params["role"] = "inbox"
            params["unread"] = "true"
        if since:
            params["after"] = since
        return api_request_paginated(
            "GET", "/api/v1/emails",
            params=params, limit=limit, cursor=cursor,
        )

    def get_email(self, email_id: str) -> Dict[str, Any]:
        """Recupere le detail d'un email (headers + body + attachments refs)."""
        return api_request("GET", f"/api/v1/emails/{email_id}")

    def search_emails(
        self,
        query: str,
        limit: int = 20,
        account_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Recherche plein-texte dans les emails."""
        params = {
            "account_id": self._resolve_account_id(account_id),
            "any_email": query,
        }
        return api_request_paginated(
            "GET", "/api/v1/emails",
            params=params, limit=limit,
        )

    def list_folders(self, account_id: Optional[str] = None) -> Dict[str, Any]:
        """Liste les dossiers / labels du compte."""
        params = {"account_id": self._resolve_account_id(account_id)}
        return api_request("GET", "/api/v1/folders", params=params)

    def send_email(
        self,
        to: List[str],
        subject: str,
        body: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        reply_to: Optional[str] = None,
        plain_text: bool = True,
        account_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Envoie un email.

        Args:
            to: Liste d'adresses email (strings).
            subject: Objet.
            body: Corps du message (texte brut par defaut).
            cc, bcc: Listes d'adresses additionnelles.
            reply_to: provider_id d'un email pour en faire une reponse (thread).
            plain_text: Si True, envoie en text/plain (header). Sinon HTML.
        """
        def _recipients(addrs: List[str]) -> List[Dict[str, str]]:
            return [{"identifier": a, "display_name": a} for a in addrs]

        payload: Dict[str, Any] = {
            "account_id": self._resolve_account_id(account_id),
            "subject": subject,
            "body": body,
            "to": _recipients(to),
        }
        if cc:
            payload["cc"] = _recipients(cc)
        if bcc:
            payload["bcc"] = _recipients(bcc)
        if reply_to:
            payload["reply_to"] = reply_to
        if plain_text:
            payload["custom_headers"] = [
                {"name": "Content-Type", "value": "text/plain; charset=utf-8"}
            ]

        return api_request("POST", "/api/v1/emails", json_data=payload)

    # ------------------------------------------------------------------ #
    # CALENDAR
    # ------------------------------------------------------------------ #

    def list_calendars(self, account_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Liste les calendriers du compte.

        Prerequis : scopes Calendars.* actives dans Unipile Settings ->
        Microsoft OAuth + reconnect du compte. Voir docs/operators/unipile-outlook.md.

        Note : l'API renvoie les calendriers dans `data`, pas `items` comme
        les autres endpoints. On normalise la reponse.
        """
        params = {"account_id": self._resolve_account_id(account_id)}
        r = api_request("GET", "/api/v1/calendars", params=params)
        # Normalise data -> items pour coherence avec le reste du client
        if "data" in r and "items" not in r:
            r["items"] = r["data"]
        return r

    def get_default_calendar_id(self, account_id: Optional[str] = None) -> str:
        """Retourne l'ID du calendrier par defaut du compte (is_default=true)."""
        cals = self.list_calendars(account_id=account_id)
        items = cals.get("items", [])
        for c in items:
            if c.get("is_default"):
                return c["id"]
        if items:
            return items[0]["id"]
        raise ValueError("Aucun calendrier trouve sur ce compte")

    def list_events(
        self,
        calendar_id: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 50,
        account_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Liste les events d'un calendrier.

        Si calendar_id non fourni, utilise le primary du compte.
        """
        acct = self._resolve_account_id(account_id)
        params: Dict[str, Any] = {"account_id": acct}
        # Les dates doivent etre en ISO 8601 complet (.sssZ)
        if date_from:
            params["min_start_time"] = _to_iso_full(date_from)
        if date_to:
            params["max_start_time"] = _to_iso_full(date_to, end_of_day=True)

        if not calendar_id:
            calendar_id = self.get_default_calendar_id(account_id=acct)
        endpoint = f"/api/v1/calendars/{calendar_id}/events"
        r = api_request_paginated("GET", endpoint, params=params, limit=limit)
        # Normalise data -> items
        if "data" in r and "items" not in r:
            r["items"] = r["data"]
        return r

    def create_event(
        self,
        title: str,
        start: str,
        end: str,
        attendees: Optional[List[str]] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        calendar_id: Optional[str] = None,
        video_link: bool = True,
        account_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Cree un event calendrier.

        Args:
            title: Titre.
            start: ISO datetime ("2026-04-15T14:00:00" ou avec timezone).
            end: ISO datetime.
            attendees: Liste d'emails des participants.
            description: Corps.
            location: Lieu physique OU "visio" pour demander un lien Teams.
            video_link: Si True, ajoute un lien Teams (Outlook) / Meet (Google).
        """
        acct = self._resolve_account_id(account_id)
        # Format attendu par Unipile : start/end nestes avec date_time + time_zone
        payload: Dict[str, Any] = {
            "account_id": acct,
            "title": title,
            "start": {"date_time": _to_iso_full(start), "time_zone": "UTC"},
            "end": {"date_time": _to_iso_full(end), "time_zone": "UTC"},
        }
        if description:
            payload["body"] = {"content": description, "content_type": "text"}
        if location and location != "visio":
            payload["location"] = location
        if attendees:
            payload["attendees"] = [
                {"email": a, "display_name": a, "type": "required"}
                for a in attendees
            ]
        if video_link:
            # Microsoft Teams pour Outlook
            payload["online_meeting_provider"] = "teamsForBusiness"

        if not calendar_id:
            calendar_id = self.get_default_calendar_id(account_id=acct)
        endpoint = f"/api/v1/calendars/{calendar_id}/events"
        return api_request("POST", endpoint, json_data=payload)

    def delete_event(self, event_id: str, calendar_id: str) -> Dict[str, Any]:
        """Supprime un event. calendar_id requis."""
        return api_request("DELETE", f"/api/v1/calendars/{calendar_id}/events/{event_id}")

    def check_availability(
        self,
        date_from: str,
        date_to: str,
        account_id: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        """
        Derive la dispo d'un compte sur une plage en listant les events.

        Retourne une liste de creneaux OCCUPES [{start, end, title}] que
        l'appelant croisera avec sa logique de creneaux souhaites.
        """
        data = self.list_events(
            date_from=date_from,
            date_to=date_to,
            limit=200,
            account_id=account_id,
        )
        busy = []
        for ev in data.get("items", []):
            s = ev.get("start", {})
            e = ev.get("end", {})
            busy.append({
                "start": s.get("date_time") if isinstance(s, dict) else s,
                "end": e.get("date_time") if isinstance(e, dict) else e,
                "title": ev.get("title", ""),
            })
        return busy


# ---------------------------------------------------------------------- #
# Formatters
# ---------------------------------------------------------------------- #

def format_emails(data: Dict[str, Any]) -> str:
    items = data.get("items", [])
    if not items:
        return "Aucun email."
    lines = [f"{len(items)} email(s):\n"]
    for i, m in enumerate(items, 1):
        email_id = m.get("id", "N/A")
        subject = m.get("subject", "(sans objet)")
        sender = m.get("from_attendee", {})
        sender_str = sender.get("identifier") or sender.get("display_name") or "?"
        date = m.get("date", m.get("timestamp", ""))
        unread = m.get("is_unread", m.get("unread", False))
        marker = "*" if unread else " "
        lines.append(f"{marker} {i:>3}. [{date[:16]}] {sender_str}")
        lines.append(f"        {subject[:80]}")
        lines.append(f"        ID: {email_id}")
        lines.append("")
    if data.get("cursor"):
        lines.append(f"Page suivante: --cursor \"{data['cursor']}\"")
    return "\n".join(lines)


def format_events(data: Dict[str, Any]) -> str:
    items = data.get("items") or data.get("data") or []
    if not items:
        return "Aucun event."
    lines = [f"{len(items)} event(s):\n"]
    for i, ev in enumerate(items, 1):
        title = ev.get("title", "(sans titre)")
        start = ev.get("start", {})
        end = ev.get("end", {})
        start_s = start.get("date_time", "")[:16] if isinstance(start, dict) else str(start)[:16]
        end_s = end.get("date_time", "")[:16] if isinstance(end, dict) else str(end)[:16]
        attendees = ev.get("attendees", [])
        lines.append(f"{i:>3}. {title}")
        lines.append(f"     {start_s} -> {end_s}")
        if ev.get("location"):
            lines.append(f"     Lieu: {ev['location']}")
        if attendees:
            names = ", ".join(
                (a.get("display_name") or a.get("email") or "?")
                for a in attendees[:5]
            )
            lines.append(f"     Participants: {names}")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------- #
# CLI
# ---------------------------------------------------------------------- #

def main():
    parser = argparse.ArgumentParser(description="Unipile Outlook Client — Email + Calendar")
    parser.add_argument("--account-id", help="ID du compte email/calendar")
    parser.add_argument("--user",
                        help="Raccourci : charge l'account_id depuis services.unipile-outlook.<user>")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("accounts", help="Lister tous les comptes connectes")

    # Email
    el = sub.add_parser("emails-list", help="Lister les emails")
    el.add_argument("--folder", help="INBOX, SENT, DRAFTS, ...")
    el.add_argument("--unread-only", action="store_true")
    el.add_argument("--since", help="Date ISO (2026-04-01)")
    el.add_argument("--limit", type=int, default=20)
    el.add_argument("--cursor")

    eg = sub.add_parser("email-get", help="Detail d'un email")
    eg.add_argument("email_id")

    es = sub.add_parser("email-search", help="Recherche plein-texte")
    es.add_argument("--query", required=True)
    es.add_argument("--limit", type=int, default=20)

    sub.add_parser("folders", help="Lister les dossiers/labels")

    esnd = sub.add_parser("email-send", help="Envoyer un email")
    esnd.add_argument("--to", required=True, help="Emails separes par virgule")
    esnd.add_argument("--subject", required=True)
    esnd.add_argument("--body", required=True)
    esnd.add_argument("--cc", help="Emails separes par virgule")
    esnd.add_argument("--bcc")
    esnd.add_argument("--reply-to", help="provider_id d'un email a repondre")
    esnd.add_argument("--html", action="store_true", help="Envoyer en HTML au lieu de text/plain")

    # Calendar
    sub.add_parser("calendars-list", help="Lister les calendriers")

    evl = sub.add_parser("events-list", help="Lister les events")
    evl.add_argument("--calendar-id")
    evl.add_argument("--from", dest="date_from", help="ISO date/datetime")
    evl.add_argument("--to", dest="date_to", help="ISO date/datetime")
    evl.add_argument("--limit", type=int, default=50)

    evc = sub.add_parser("event-create", help="Creer un event")
    evc.add_argument("--title", required=True)
    evc.add_argument("--start", required=True, help="ISO datetime")
    evc.add_argument("--end", required=True, help="ISO datetime")
    evc.add_argument("--attendees", help="Emails separes par virgule")
    evc.add_argument("--description")
    evc.add_argument("--location", help="Adresse OU 'visio'")
    evc.add_argument("--calendar-id")
    evc.add_argument("--no-video", action="store_true")

    evd = sub.add_parser("event-delete", help="Supprimer un event")
    evd.add_argument("event_id")
    evd.add_argument("--calendar-id", required=True)

    av = sub.add_parser("availability", help="Creneaux OCCUPES sur une plage")
    av.add_argument("--from", dest="date_from", required=True)
    av.add_argument("--to", dest="date_to", required=True)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        client = UnipileOutlookClient(account_id=args.account_id, user=args.user)

        if args.command == "accounts":
            data = client.list_accounts()
            print(json.dumps(data, indent=2, ensure_ascii=False))

        elif args.command == "emails-list":
            data = client.list_emails(
                folder=args.folder,
                unread_only=args.unread_only,
                since=args.since,
                limit=args.limit,
                cursor=args.cursor,
            )
            print(format_emails(data))

        elif args.command == "email-get":
            data = client.get_email(args.email_id)
            print(json.dumps(data, indent=2, ensure_ascii=False))

        elif args.command == "email-search":
            data = client.search_emails(query=args.query, limit=args.limit)
            print(format_emails(data))

        elif args.command == "folders":
            data = client.list_folders()
            print(json.dumps(data, indent=2, ensure_ascii=False))

        elif args.command == "email-send":
            to_list = [x.strip() for x in args.to.split(",") if x.strip()]
            cc_list = [x.strip() for x in args.cc.split(",")] if args.cc else None
            bcc_list = [x.strip() for x in args.bcc.split(",")] if args.bcc else None
            print(f"Envoi email -> {to_list} ...")
            result = client.send_email(
                to=to_list,
                subject=args.subject,
                body=args.body,
                cc=cc_list,
                bcc=bcc_list,
                reply_to=args.reply_to,
                plain_text=not args.html,
            )
            print("[OK] Email envoye.")
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "calendars-list":
            data = client.list_calendars()
            print(json.dumps(data, indent=2, ensure_ascii=False))

        elif args.command == "events-list":
            data = client.list_events(
                calendar_id=args.calendar_id,
                date_from=args.date_from,
                date_to=args.date_to,
                limit=args.limit,
            )
            print(format_events(data))

        elif args.command == "event-create":
            atts = [x.strip() for x in args.attendees.split(",")] if args.attendees else None
            print(f"Creation event '{args.title}' {args.start} -> {args.end} ...")
            result = client.create_event(
                title=args.title,
                start=args.start,
                end=args.end,
                attendees=atts,
                description=args.description,
                location=args.location,
                calendar_id=args.calendar_id,
                video_link=not args.no_video,
            )
            print("[OK] Event cree.")
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "event-delete":
            result = client.delete_event(args.event_id, calendar_id=args.calendar_id)
            print("[OK] Event supprime.")
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "availability":
            busy = client.check_availability(
                date_from=args.date_from,
                date_to=args.date_to,
            )
            if not busy:
                print("Aucun creneau occupe sur la plage — tout est libre.")
            else:
                print(f"{len(busy)} creneau(x) occupe(s):")
                for b in busy:
                    print(f"  {b['start']} -> {b['end']}  {b['title']}")

    except ValueError as e:
        print(f"ERREUR CONFIG: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERREUR: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
