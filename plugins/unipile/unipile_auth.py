#!/usr/bin/env python3
"""
Module d'authentification partage pour les services Unipile.

Gere la resolution de la configuration et les appels API
pour tous les clients (LinkedIn, Messaging).
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin

import requests


def find_plugin_root(start_path: Path = None) -> Path:
    """
    Remonte les dossiers en cherchant `.claude-plugin/` pour trouver
    la racine du plugin unipile.
    """
    if start_path is None:
        start_path = Path(__file__).parent

    current = start_path.resolve()
    while current != current.parent:
        if (current / ".claude-plugin").is_dir():
            return current
        current = current.parent

    # Fallback: dossier parent de clients/
    return Path(__file__).parent.parent


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Charge unipile-config.json depuis :
    1. Argument config_path
    2. Env var UNIPILE_CONFIG_PATH
    3. unipile-config.json a la racine du plugin
    """
    if config_path is None:
        config_path = os.environ.get("UNIPILE_CONFIG_PATH")

    if config_path is None:
        plugin_root = find_plugin_root()
        config_path = str(plugin_root / "unipile-config.json")

    path = Path(config_path)
    if not path.exists():
        return {}

    with open(path) as f:
        return json.load(f)


def get_api_key(config_path: Optional[str] = None) -> str:
    """
    Retourne l'API key (access token) depuis :
    1. Env var UNIPILE_API_KEY
    2. Champ api_key dans unipile-config.json
    """
    env_key = os.environ.get("UNIPILE_API_KEY")
    if env_key:
        return env_key

    config = load_config(config_path)
    api_key = config.get("api_key", "")
    if not api_key or api_key == "YOUR_ACCESS_TOKEN":
        raise ValueError(
            "API key Unipile non configuree.\n"
            "Options:\n"
            "  1. Definir UNIPILE_API_KEY dans l'environnement\n"
            "  2. Renseigner api_key dans unipile-config.json"
        )
    return api_key


def get_dsn(config_path: Optional[str] = None) -> str:
    """
    Retourne le DSN (base URL de l'API) depuis :
    1. Env var UNIPILE_DSN
    2. Champ dsn dans unipile-config.json

    Si le DSN n'a pas de scheme http/https, on prefixe https:// par defaut.
    """
    env_dsn = os.environ.get("UNIPILE_DSN")
    if env_dsn:
        return _ensure_scheme(env_dsn).rstrip("/")

    config = load_config(config_path)
    dsn = config.get("dsn", "")
    if not dsn or dsn == "YOUR_DSN_URL":
        raise ValueError(
            "DSN Unipile non configure.\n"
            "Options:\n"
            "  1. Definir UNIPILE_DSN dans l'environnement\n"
            "  2. Renseigner dsn dans unipile-config.json"
        )
    return _ensure_scheme(dsn).rstrip("/")


def _ensure_scheme(url: str) -> str:
    """Prefixe https:// si l'URL n'a pas deja un scheme http(s)://."""
    stripped = url.strip()
    lowered = stripped.lower()
    if lowered.startswith("http://") or lowered.startswith("https://"):
        return stripped
    return f"https://{stripped}"


def get_service_config(service_name: str) -> Dict[str, Any]:
    """
    Recupere la configuration d'un service specifique depuis unipile-config.json.

    Args:
        service_name: Nom du service (unipile-linkedin, unipile-messaging)

    Returns:
        Dict de configuration du service
    """
    config = load_config()
    return config.get("services", {}).get(service_name, {})


def api_request(
    method: str,
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    config_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Effectue un appel API Unipile avec authentification Bearer.

    Args:
        method: Methode HTTP (GET, POST, PUT, DELETE)
        endpoint: Chemin de l'endpoint (ex: /api/v1/users/123)
        params: Parametres query string
        json_data: Corps JSON de la requete
        config_path: Chemin vers unipile-config.json (optionnel)

    Returns:
        Dict de la reponse JSON

    Raises:
        requests.HTTPError: Si la reponse indique une erreur
    """
    dsn = get_dsn(config_path)
    api_key = get_api_key(config_path)

    url = f"{dsn}{endpoint}"

    headers = {
        "Accept": "application/json",
        "X-API-KEY": api_key,
    }

    if json_data is not None:
        headers["Content-Type"] = "application/json"

    response = requests.request(
        method=method.upper(),
        url=url,
        headers=headers,
        params=params,
        json=json_data,
        timeout=30,
    )

    if response.status_code >= 400:
        try:
            error_body = response.json()
        except Exception:
            error_body = response.text
        raise requests.HTTPError(
            f"API {response.status_code}: {error_body}",
            response=response,
        )

    if response.status_code == 204:
        return {"status": "ok"}

    return response.json()


def api_request_paginated(
    method: str,
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    limit: int = 10,
    cursor: Optional[str] = None,
    config_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Appel API avec gestion de la pagination cursor.

    Retourne la reponse brute (avec cursor pour la page suivante).
    Le client decide s'il veut iterer.

    Args:
        method: Methode HTTP
        endpoint: Chemin de l'endpoint
        params: Parametres query string additionnels
        json_data: Corps JSON
        limit: Nombre de resultats par page
        cursor: Cursor pour la page suivante
        config_path: Chemin config

    Returns:
        Dict avec les items et le cursor de pagination
    """
    if params is None:
        params = {}
    params["limit"] = limit
    if cursor:
        params["cursor"] = cursor

    return api_request(
        method=method,
        endpoint=endpoint,
        params=params,
        json_data=json_data,
        config_path=config_path,
    )


def check_setup() -> Dict[str, str]:
    """
    Verifie l'etat de l'installation.

    Returns:
        Dict avec les statuts: {venv_ok, deps_ok, config_ok, api_ok}
        Valeurs: 'ok', 'warn', 'fail'
    """
    import subprocess
    plugin_root = find_plugin_root()
    status = {}

    # venv
    venv_path = plugin_root / "venv"
    status["venv_ok"] = "ok" if venv_path.is_dir() else "fail"

    # deps
    if status["venv_ok"] == "ok":
        python_path = venv_path / "bin" / "python"
        try:
            result = subprocess.run(
                [str(python_path), "-c", "import requests; print('ok')"],
                capture_output=True, text=True, timeout=10
            )
            status["deps_ok"] = "ok" if result.returncode == 0 and "ok" in result.stdout else "fail"
        except Exception:
            status["deps_ok"] = "fail"
    else:
        status["deps_ok"] = "fail"

    # config
    config_path = plugin_root / "unipile-config.json"
    if config_path.exists():
        try:
            config = load_config(str(config_path))
            dsn = config.get("dsn", "")
            api_key = config.get("api_key", "")
            if dsn and dsn != "YOUR_DSN_URL" and api_key and api_key != "YOUR_ACCESS_TOKEN":
                status["config_ok"] = "ok"
            else:
                status["config_ok"] = "warn"
        except Exception:
            status["config_ok"] = "warn"
    else:
        status["config_ok"] = "fail"

    # api connectivity
    if status["config_ok"] == "ok":
        try:
            result = api_request("GET", "/api/v1/accounts", config_path=str(config_path))
            status["api_ok"] = "ok"
        except Exception:
            status["api_ok"] = "fail"
    else:
        status["api_ok"] = "fail"

    return status
