#!/usr/bin/env python3
"""
Unipile LinkedIn Client - Recherche de leads et enrichissement de profils.

Usage:
    python linkedin_client.py search-people --keywords "CTO" --limit 5
    python linkedin_client.py search-companies --keywords "SaaS" --limit 5
    python linkedin_client.py search-params --type locations --query "Paris"
    python linkedin_client.py profile PROFILE_ID
    python linkedin_client.py company COMPANY_ID
    python linkedin_client.py employees --company COMPANY_ID --limit 10
    python linkedin_client.py contacts --limit 20

Options communes:
    --account-id ID     ID du compte LinkedIn connecte dans Unipile
    --limit N           Nombre de resultats (defaut: 10)
    --cursor CURSOR     Cursor pour pagination
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, Optional, List

sys.path.insert(0, str(Path(__file__).parent))

from unipile_auth import api_request, api_request_paginated, get_service_config


class UnipileLinkedInClient:
    """Client pour les operations LinkedIn via l'API Unipile."""

    def __init__(self, account_id: Optional[str] = None):
        """Initialise le client avec l'account_id optionnel."""
        config = get_service_config("unipile-linkedin")
        self.default_account_id = account_id or config.get("default_account_id")

    def _resolve_account_id(self, account_id: Optional[str] = None) -> Optional[str]:
        """Resout l'account_id : argument > config."""
        return account_id or self.default_account_id

    def search_people(
        self,
        keywords: Optional[str] = None,
        location: Optional[str] = None,
        industry: Optional[str] = None,
        job_title: Optional[str] = None,
        company: Optional[str] = None,
        network: Optional[str] = None,
        api: str = "classic",
        account_id: Optional[str] = None,
        limit: int = 10,
        cursor: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Recherche de personnes sur LinkedIn.

        Args:
            keywords: Mots-cles de recherche
            location: Filtre localisation (ID ou nom)
            industry: Filtre industrie (ID)
            job_title: Filtre titre de poste
            company: Filtre entreprise (ID ou nom)
            network: Filtre reseau (F=1st, S=2nd, O=3rd+)
            api: Type d'API (classic, sales_navigator, recruiter)
            account_id: ID du compte LinkedIn
            limit: Nombre de resultats
            cursor: Cursor pour pagination
        """
        body = {"category": "people", "api": api}
        if keywords:
            body["keywords"] = keywords
        if location:
            body["location"] = location
        if industry:
            body["industry"] = industry
        if job_title:
            body["job_title"] = job_title
        if company:
            body["current_company"] = company
        if network:
            body["network"] = network

        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        acct = self._resolve_account_id(account_id)
        if acct:
            params["account_id"] = acct

        return api_request("POST", "/api/v1/linkedin/search", params=params, json_data=body)

    def search_companies(
        self,
        keywords: Optional[str] = None,
        location: Optional[str] = None,
        industry: Optional[str] = None,
        company_size: Optional[str] = None,
        api: str = "classic",
        account_id: Optional[str] = None,
        limit: int = 10,
        cursor: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Recherche d'entreprises sur LinkedIn."""
        body = {"category": "companies", "api": api}
        if keywords:
            body["keywords"] = keywords
        if location:
            body["location"] = location
        if industry:
            body["industry"] = industry
        if company_size:
            body["company_size"] = company_size

        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        acct = self._resolve_account_id(account_id)
        if acct:
            params["account_id"] = acct

        return api_request("POST", "/api/v1/linkedin/search", params=params, json_data=body)

    def search_params(
        self,
        param_type: str,
        query: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Resout les IDs de filtres LinkedIn (locations, industries, etc.).

        Args:
            param_type: Type de parametre (locations, industries, companies, schools, etc.)
            query: Texte de recherche pour filtrer
            account_id: ID du compte LinkedIn
        """
        params = {"type": param_type}
        if query:
            params["query"] = query

        acct = self._resolve_account_id(account_id)
        if acct:
            params["account_id"] = acct

        return api_request("GET", "/api/v1/linkedin/search/parameters", params=params)

    def get_profile(
        self,
        profile_id: str,
        account_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Recupere le profil complet d'une personne.

        Args:
            profile_id: ID LinkedIn ou URL du profil
            account_id: ID du compte LinkedIn
        """
        params = {"linkedin_sections": "*"}

        acct = self._resolve_account_id(account_id)
        if acct:
            params["account_id"] = acct

        return api_request("GET", f"/api/v1/users/{profile_id}", params=params)

    def get_company(
        self,
        company_id: str,
        account_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Recupere la page entreprise LinkedIn.

        Args:
            company_id: ID ou slug LinkedIn de l'entreprise
            account_id: ID du compte LinkedIn
        """
        params = {}
        acct = self._resolve_account_id(account_id)
        if acct:
            params["account_id"] = acct

        return api_request("GET", f"/api/v1/linkedin/company/{company_id}", params=params)

    def get_employees(
        self,
        company_id: str,
        keywords: Optional[str] = None,
        account_id: Optional[str] = None,
        limit: int = 10,
        cursor: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Trouve les employes d'une entreprise.

        Args:
            company_id: ID de l'entreprise
            keywords: Filtre par mots-cles (poste, competence...)
            account_id: ID du compte LinkedIn
            limit: Nombre de resultats
            cursor: Cursor pour pagination
        """
        body = {
            "category": "people",
            "current_company": company_id,
            "api": "classic",
        }
        if keywords:
            body["keywords"] = keywords

        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        acct = self._resolve_account_id(account_id)
        if acct:
            params["account_id"] = acct

        return api_request("POST", "/api/v1/linkedin/search", params=params, json_data=body)

    def get_contacts(
        self,
        account_id: Optional[str] = None,
        limit: int = 10,
        cursor: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Liste les connexions LinkedIn (contacts/relations).

        Args:
            account_id: ID du compte LinkedIn
            limit: Nombre de resultats
            cursor: Cursor pour pagination
        """
        params = {}
        acct = self._resolve_account_id(account_id)
        if acct:
            params["account_id"] = acct

        return api_request_paginated(
            "GET", "/api/v1/users/relations",
            params=params, limit=limit, cursor=cursor,
        )


def format_search_results(data: Dict[str, Any], result_type: str = "people") -> str:
    """Formate les resultats de recherche en tableau lisible."""
    items = data.get("items", [])
    if not items:
        return "Aucun resultat."

    lines = []
    lines.append(f"{len(items)} resultat(s) {result_type}:\n")

    for i, item in enumerate(items, 1):
        if result_type == "people":
            name = item.get("name", "N/A")
            headline = item.get("headline", "")
            location = item.get("location", "")
            lines.append(f"{i:>3}. {name}")
            if headline:
                lines.append(f"     {headline}")
            if location:
                lines.append(f"     {location}")
            profile_id = item.get("id", item.get("provider_id", ""))
            if profile_id:
                lines.append(f"     ID: {profile_id}")
            lines.append("")
        else:
            name = item.get("name", "N/A")
            industry = item.get("industry", "")
            size = item.get("company_size", "")
            lines.append(f"{i:>3}. {name}")
            if industry:
                lines.append(f"     Industrie: {industry}")
            if size:
                lines.append(f"     Taille: {size}")
            company_id = item.get("id", item.get("provider_id", ""))
            if company_id:
                lines.append(f"     ID: {company_id}")
            lines.append("")

    cursor = data.get("cursor")
    if cursor:
        lines.append(f"Page suivante: --cursor \"{cursor}\"")

    return "\n".join(lines)


def format_profile(data: Dict[str, Any]) -> str:
    """Formate un profil LinkedIn."""
    lines = []
    name = data.get("name", "N/A")
    headline = data.get("headline", "")
    location = data.get("location", "")
    summary = data.get("summary", "")

    lines.append(f"Profil: {name}")
    if headline:
        lines.append(f"   Titre: {headline}")
    if location:
        lines.append(f"   Localisation: {location}")
    if summary:
        lines.append(f"   Resume: {summary[:200]}{'...' if len(summary) > 200 else ''}")

    # Experiences
    experiences = data.get("experiences", [])
    if experiences:
        lines.append(f"\n   Experiences ({len(experiences)}):")
        for exp in experiences[:5]:
            title = exp.get("title", "N/A")
            company = exp.get("company_name", "")
            period = exp.get("date_range", "")
            lines.append(f"      - {title} @ {company} ({period})")

    # Education
    education = data.get("education", [])
    if education:
        lines.append(f"\n   Formation ({len(education)}):")
        for edu in education[:3]:
            school = edu.get("school_name", "N/A")
            degree = edu.get("degree", "")
            lines.append(f"      - {school} ({degree})")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Unipile LinkedIn Client")
    parser.add_argument("--account-id", help="ID du compte LinkedIn connecte")
    subparsers = parser.add_subparsers(dest="command", help="Commande")

    # search-people
    sp = subparsers.add_parser("search-people", help="Recherche de personnes")
    sp.add_argument("--keywords", help="Mots-cles de recherche")
    sp.add_argument("--location", help="Filtre localisation")
    sp.add_argument("--industry", help="Filtre industrie")
    sp.add_argument("--job-title", help="Filtre titre de poste")
    sp.add_argument("--company", help="Filtre entreprise (ID)")
    sp.add_argument("--network", choices=["F", "S", "O"], help="Filtre reseau (F=1st, S=2nd, O=3rd+)")
    sp.add_argument("--api", choices=["classic", "sales_navigator", "recruiter"], default="classic")
    sp.add_argument("--limit", type=int, default=10)
    sp.add_argument("--cursor", help="Cursor pagination")

    # search-companies
    sc = subparsers.add_parser("search-companies", help="Recherche d'entreprises")
    sc.add_argument("--keywords", help="Mots-cles de recherche")
    sc.add_argument("--location", help="Filtre localisation")
    sc.add_argument("--industry", help="Filtre industrie")
    sc.add_argument("--company-size", help="Filtre taille entreprise")
    sc.add_argument("--api", choices=["classic", "sales_navigator", "recruiter"], default="classic")
    sc.add_argument("--limit", type=int, default=10)
    sc.add_argument("--cursor", help="Cursor pagination")

    # search-params
    spp = subparsers.add_parser("search-params", help="Resoudre IDs de filtres")
    spp.add_argument("--type", dest="param_type", required=True,
                     help="Type: locations, industries, companies, schools, etc.")
    spp.add_argument("--query", help="Texte de recherche")

    # profile
    prof = subparsers.add_parser("profile", help="Profil complet d'une personne")
    prof.add_argument("profile_id", help="ID ou URL du profil LinkedIn")

    # company
    comp = subparsers.add_parser("company", help="Page entreprise LinkedIn")
    comp.add_argument("company_id", help="ID ou slug de l'entreprise")

    # employees
    emp = subparsers.add_parser("employees", help="Employes d'une entreprise")
    emp.add_argument("--company", required=True, help="ID de l'entreprise")
    emp.add_argument("--keywords", help="Filtre par mots-cles")
    emp.add_argument("--limit", type=int, default=10)
    emp.add_argument("--cursor", help="Cursor pagination")

    # contacts
    cont = subparsers.add_parser("contacts", help="Lister ses connexions")
    cont.add_argument("--limit", type=int, default=10)
    cont.add_argument("--cursor", help="Cursor pagination")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        client = UnipileLinkedInClient(account_id=args.account_id)

        if args.command == "search-people":
            data = client.search_people(
                keywords=args.keywords,
                location=args.location,
                industry=args.industry,
                job_title=args.job_title,
                company=args.company,
                network=args.network,
                api=args.api,
                limit=args.limit,
                cursor=args.cursor,
            )
            print(format_search_results(data, "people"))

        elif args.command == "search-companies":
            data = client.search_companies(
                keywords=args.keywords,
                location=args.location,
                industry=args.industry,
                company_size=args.company_size,
                api=args.api,
                limit=args.limit,
                cursor=args.cursor,
            )
            print(format_search_results(data, "companies"))

        elif args.command == "search-params":
            data = client.search_params(
                param_type=args.param_type,
                query=args.query,
            )
            items = data.get("items", data)
            print(json.dumps(items, indent=2, ensure_ascii=False))

        elif args.command == "profile":
            data = client.get_profile(args.profile_id)
            print(format_profile(data))

        elif args.command == "company":
            data = client.get_company(args.company_id)
            print(json.dumps(data, indent=2, ensure_ascii=False))

        elif args.command == "employees":
            data = client.get_employees(
                company_id=args.company,
                keywords=args.keywords,
                limit=args.limit,
                cursor=args.cursor,
            )
            print(format_search_results(data, "people"))

        elif args.command == "contacts":
            data = client.get_contacts(
                limit=args.limit,
                cursor=args.cursor,
            )
            items = data.get("items", [])
            if not items:
                print("Aucun contact trouve.")
            else:
                print(f"{len(items)} contact(s):\n")
                for i, c in enumerate(items, 1):
                    name = c.get("name", "N/A")
                    headline = c.get("headline", "")
                    print(f"{i:>3}. {name}")
                    if headline:
                        print(f"     {headline}")
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
