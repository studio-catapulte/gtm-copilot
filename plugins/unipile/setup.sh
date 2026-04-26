#!/usr/bin/env bash
set -euo pipefail

PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PLUGIN_DIR/venv"
REQUIREMENTS="$PLUGIN_DIR/requirements.txt"

if ! command -v python3 >/dev/null 2>&1; then
    echo "Erreur : python3 introuvable dans le PATH." >&2
    echo "Installe Python 3 (https://www.python.org/) puis relance ce script." >&2
    exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "Création du venv dans $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
else
    echo "Venv déjà présent dans $VENV_DIR (réutilisé)."
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

if [ ! -f "$REQUIREMENTS" ]; then
    echo "Erreur : $REQUIREMENTS introuvable." >&2
    exit 1
fi

echo "Installation des dépendances depuis requirements.txt..."
pip install --quiet --upgrade pip
pip install --quiet -r "$REQUIREMENTS"

echo ""
echo "Setup Unipile terminé avec succès."
echo "Venv : $VENV_DIR"
echo "Pour activer manuellement : source \"$VENV_DIR/bin/activate\""
