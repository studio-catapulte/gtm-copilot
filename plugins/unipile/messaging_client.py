#!/usr/bin/env python3
"""
Unipile Messaging Client - Outreach multi-canal et messaging.

Usage:
    python messaging_client.py accounts                                    # Lister les comptes connectes
    python messaging_client.py chats --limit 10                            # Lister les conversations
    python messaging_client.py messages CHAT_ID --limit 20                 # Messages d'une conversation
    python messaging_client.py send CHAT_ID --text "Bonjour !"             # Envoyer un message
    python messaging_client.py new-chat --attendee-id PROFILE_ID --text "Hello"  # Nouvelle conversation
    python messaging_client.py invite PROFILE_ID --note "Bonjour..."       # Invitation LinkedIn
    python messaging_client.py inmail PROFILE_ID --subject "..." --text "..."  # InMail
    python messaging_client.py ig-profile USERNAME                         # Profil Instagram
    python messaging_client.py ig-posts USERNAME --limit 5                 # Posts Instagram

Options communes:
    --account-id ID         ID du compte connecte dans Unipile
    --provider PROVIDER     Provider: LINKEDIN, WHATSAPP, INSTAGRAM
    --limit N               Nombre de resultats (defaut: 10)
    --cursor CURSOR         Cursor pour pagination
"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, Optional, List

sys.path.insert(0, str(Path(__file__).parent))

from unipile_auth import api_request, api_request_paginated, get_service_config


class UnipileMessagingClient:
    """Client pour le messaging multi-canal via l'API Unipile."""

    def __init__(self, account_id: Optional[str] = None):
        """Initialise le client avec l'account_id optionnel."""
        config = get_service_config("unipile-messaging")
        self.default_account_id = (
            account_id
            or os.environ.get("UNIPILE_ACCOUNT_ID")
            or config.get("default_account_id")
        )

    def _resolve_account_id(self, account_id: Optional[str] = None) -> Optional[str]:
        """Resout l'account_id : argument > config."""
        return account_id or self.default_account_id

    def list_accounts(
        self,
        limit: int = 50,
        cursor: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Liste les comptes connectes dans Unipile."""
        return api_request_paginated(
            "GET", "/api/v1/accounts",
            limit=limit, cursor=cursor,
        )

    def list_chats(
        self,
        account_id: Optional[str] = None,
        provider: Optional[str] = None,
        limit: int = 10,
        cursor: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Liste les conversations.

        Args:
            account_id: Filtre par compte
            provider: Filtre par provider (LINKEDIN, WHATSAPP, INSTAGRAM)
            limit: Nombre de resultats
            cursor: Cursor pour pagination
        """
        params = {}
        acct = self._resolve_account_id(account_id)
        if acct:
            params["account_id"] = acct
        if provider:
            params["provider"] = provider.upper()

        return api_request_paginated(
            "GET", "/api/v1/chats",
            params=params, limit=limit, cursor=cursor,
        )

    def get_messages(
        self,
        chat_id: str,
        limit: int = 20,
        cursor: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Recupere les messages d'une conversation.

        Args:
            chat_id: ID de la conversation
            limit: Nombre de messages
            cursor: Cursor pour pagination
        """
        return api_request_paginated(
            "GET", f"/api/v1/chats/{chat_id}/messages",
            limit=limit, cursor=cursor,
        )

    def send_message(
        self,
        chat_id: str,
        text: str,
    ) -> Dict[str, Any]:
        """
        Envoie un message dans une conversation existante.

        Args:
            chat_id: ID de la conversation
            text: Contenu du message
        """
        body = {"text": text}
        return api_request("POST", f"/api/v1/chats/{chat_id}/messages", json_data=body)

    def new_chat(
        self,
        attendee_id: str,
        text: str,
        account_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Demarre une nouvelle conversation.

        Args:
            attendee_id: ID du destinataire (profil LinkedIn, numero WhatsApp, etc.)
            text: Premier message
            account_id: ID du compte emetteur
        """
        body = {
            "attendees_ids": [attendee_id],
            "text": text,
        }
        acct = self._resolve_account_id(account_id)
        if acct:
            body["account_id"] = acct

        return api_request("POST", "/api/v1/chats", json_data=body)

    def send_invite(
        self,
        profile_id: str,
        note: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Envoie une invitation LinkedIn.

        Args:
            profile_id: ID du profil LinkedIn a inviter
            note: Note d'accompagnement (max 300 caracteres)
            account_id: ID du compte LinkedIn
        """
        body = {
            "provider_id": profile_id,
        }
        if note:
            body["message"] = note

        acct = self._resolve_account_id(account_id)
        if acct:
            body["account_id"] = acct

        return api_request("POST", "/api/v1/users/invite", json_data=body)

    def send_inmail(
        self,
        profile_id: str,
        subject: str,
        text: str,
        account_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Envoie un InMail LinkedIn.

        Args:
            profile_id: ID du profil LinkedIn
            subject: Objet de l'InMail
            text: Corps du message
            account_id: ID du compte LinkedIn
        """
        body = {
            "provider_id": profile_id,
            "inmail": True,
            "subject": subject,
            "message": text,
        }

        acct = self._resolve_account_id(account_id)
        if acct:
            body["account_id"] = acct

        return api_request("POST", "/api/v1/users/invite", json_data=body)

    def get_ig_profile(
        self,
        username: str,
        account_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Recupere le profil d'un compte Instagram.

        Args:
            username: Nom d'utilisateur Instagram
            account_id: ID du compte Instagram connecte
        """
        params = {}
        acct = self._resolve_account_id(account_id)
        if acct:
            params["account_id"] = acct

        return api_request("GET", f"/api/v1/users/{username}", params=params)

    def get_ig_posts(
        self,
        username: str,
        account_id: Optional[str] = None,
        limit: int = 10,
        cursor: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Recupere les posts d'un compte Instagram.

        Args:
            username: Nom d'utilisateur Instagram
            account_id: ID du compte Instagram connecte
            limit: Nombre de posts
            cursor: Cursor pour pagination
        """
        params = {}
        acct = self._resolve_account_id(account_id)
        if acct:
            params["account_id"] = acct

        return api_request_paginated(
            "GET", f"/api/v1/users/{username}/posts",
            params=params, limit=limit, cursor=cursor,
        )


def format_chats(data: Dict[str, Any]) -> str:
    """Formate la liste des conversations."""
    items = data.get("items", [])
    if not items:
        return "Aucune conversation."

    lines = []
    lines.append(f"{len(items)} conversation(s):\n")

    for i, chat in enumerate(items, 1):
        chat_id = chat.get("id", "N/A")
        provider = chat.get("provider", "")
        name = chat.get("name", "")
        last_msg = chat.get("last_message", {})
        last_text = last_msg.get("text", "")[:60] if last_msg else ""
        timestamp = chat.get("timestamp", "")

        lines.append(f"{i:>3}. [{provider}] {name}")
        lines.append(f"     ID: {chat_id}")
        if last_text:
            lines.append(f"     Dernier msg: {last_text}{'...' if len(last_msg.get('text', '')) > 60 else ''}")
        if timestamp:
            lines.append(f"     Date: {timestamp}")
        lines.append("")

    cursor = data.get("cursor")
    if cursor:
        lines.append(f"Page suivante: --cursor \"{cursor}\"")

    return "\n".join(lines)


def format_messages(data: Dict[str, Any]) -> str:
    """Formate les messages d'une conversation."""
    items = data.get("items", [])
    if not items:
        return "Aucun message."

    lines = []
    lines.append(f"{len(items)} message(s):\n")

    for msg in items:
        sender = msg.get("sender", {}).get("name", "?")
        text = msg.get("text", "")
        timestamp = msg.get("timestamp", "")
        lines.append(f"[{timestamp}] {sender}:")
        lines.append(f"   {text}")
        lines.append("")

    cursor = data.get("cursor")
    if cursor:
        lines.append(f"Page suivante: --cursor \"{cursor}\"")

    return "\n".join(lines)


def format_accounts(data: Dict[str, Any]) -> str:
    """Formate la liste des comptes connectes."""
    items = data.get("items", [])
    if not items:
        return "Aucun compte connecte."

    lines = []
    lines.append(f"{len(items)} compte(s) connecte(s):\n")

    for i, acct in enumerate(items, 1):
        acct_id = acct.get("id", "N/A")
        provider = acct.get("type", acct.get("provider", ""))
        name = acct.get("name", "")
        status = acct.get("status", "")
        lines.append(f"{i:>3}. [{provider}] {name}")
        lines.append(f"     ID: {acct_id}")
        lines.append(f"     Status: {status}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Unipile Messaging Client")
    parser.add_argument("--account-id", help="ID du compte connecte")
    subparsers = parser.add_subparsers(dest="command", help="Commande")

    # accounts
    acc = subparsers.add_parser("accounts", help="Lister les comptes connectes")
    acc.add_argument("--limit", type=int, default=50)
    acc.add_argument("--cursor", help="Cursor pagination")

    # chats
    ch = subparsers.add_parser("chats", help="Lister les conversations")
    ch.add_argument("--provider", choices=["LINKEDIN", "WHATSAPP", "INSTAGRAM"],
                    help="Filtrer par provider")
    ch.add_argument("--limit", type=int, default=10)
    ch.add_argument("--cursor", help="Cursor pagination")

    # messages
    msg = subparsers.add_parser("messages", help="Messages d'une conversation")
    msg.add_argument("chat_id", help="ID de la conversation")
    msg.add_argument("--limit", type=int, default=20)
    msg.add_argument("--cursor", help="Cursor pagination")

    # send
    snd = subparsers.add_parser("send", help="Envoyer un message")
    snd.add_argument("chat_id", help="ID de la conversation")
    snd.add_argument("--text", required=True, help="Contenu du message")

    # new-chat
    nc = subparsers.add_parser("new-chat", help="Demarrer une conversation")
    nc.add_argument("--attendee-id", required=True, help="ID du destinataire")
    nc.add_argument("--text", required=True, help="Premier message")

    # invite
    inv = subparsers.add_parser("invite", help="Invitation LinkedIn")
    inv.add_argument("profile_id", help="ID du profil LinkedIn")
    inv.add_argument("--note", help="Note d'accompagnement (max 300 car.)")

    # inmail
    im = subparsers.add_parser("inmail", help="Envoyer un InMail")
    im.add_argument("profile_id", help="ID du profil LinkedIn")
    im.add_argument("--subject", required=True, help="Objet de l'InMail")
    im.add_argument("--text", required=True, help="Corps du message")

    # ig-profile
    igp = subparsers.add_parser("ig-profile", help="Profil Instagram")
    igp.add_argument("username", help="Nom d'utilisateur Instagram")

    # ig-posts
    igpo = subparsers.add_parser("ig-posts", help="Posts Instagram")
    igpo.add_argument("username", help="Nom d'utilisateur Instagram")
    igpo.add_argument("--limit", type=int, default=10)
    igpo.add_argument("--cursor", help="Cursor pagination")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        client = UnipileMessagingClient(account_id=args.account_id)

        if args.command == "accounts":
            data = client.list_accounts(limit=args.limit, cursor=args.cursor)
            print(format_accounts(data))

        elif args.command == "chats":
            data = client.list_chats(
                provider=args.provider,
                limit=args.limit,
                cursor=args.cursor,
            )
            print(format_chats(data))

        elif args.command == "messages":
            data = client.get_messages(
                chat_id=args.chat_id,
                limit=args.limit,
                cursor=args.cursor,
            )
            print(format_messages(data))

        elif args.command == "send":
            print(f"Envoi du message dans la conversation {args.chat_id}...")
            result = client.send_message(args.chat_id, args.text)
            print(f"[OK] Message envoye.")
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "new-chat":
            print(f"Creation d'une conversation avec {args.attendee_id}...")
            result = client.new_chat(
                attendee_id=args.attendee_id,
                text=args.text,
            )
            print(f"[OK] Conversation creee.")
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "invite":
            print(f"Envoi d'une invitation LinkedIn a {args.profile_id}...")
            result = client.send_invite(
                profile_id=args.profile_id,
                note=args.note,
            )
            print(f"[OK] Invitation envoyee.")
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "inmail":
            print(f"Envoi d'un InMail a {args.profile_id}...")
            result = client.send_inmail(
                profile_id=args.profile_id,
                subject=args.subject,
                text=args.text,
            )
            print(f"[OK] InMail envoye.")
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "ig-profile":
            data = client.get_ig_profile(args.username)
            print(json.dumps(data, indent=2, ensure_ascii=False))

        elif args.command == "ig-posts":
            data = client.get_ig_posts(
                username=args.username,
                limit=args.limit,
                cursor=args.cursor,
            )
            items = data.get("items", [])
            if not items:
                print("Aucun post trouve.")
            else:
                print(f"{len(items)} post(s):\n")
                for i, post in enumerate(items, 1):
                    text = post.get("text", post.get("caption", ""))[:80]
                    timestamp = post.get("timestamp", "")
                    likes = post.get("likes_count", "")
                    print(f"{i:>3}. [{timestamp}] {text}")
                    if likes:
                        print(f"     Likes: {likes}")
                    print()

                cursor = data.get("cursor")
                if cursor:
                    print(f"Page suivante: --cursor \"{cursor}\"")

    except ValueError as e:
        print(f"ERREUR CONFIG: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERREUR: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
