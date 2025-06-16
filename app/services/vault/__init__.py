# services/__init__.py

import os
import hvac

# Configuration globale du client Vault
#
# Utilise la variable d'environnement standard "VAULT_ADDR" pour
# déterminer l'adresse du serveur Vault. Si elle n'est pas définie,
# une valeur par défaut est utilisée.
VAULT_ADDR = os.environ.get("VAULT_ADDR", "https://127.0.0.1:8200")
VAULT_TOKEN = os.environ.get("VAULT_TOKEN", "VaultTokenToChange")

vault_client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)


def configure_client(address: str, token: str) -> None:
    """Update the global ``vault_client`` with given parameters."""
    global vault_client
    vault_client = hvac.Client(url=address, token=token)

# Importation des fonctions
from .certificates import list_certificates, get_certificate_details
from .routes import vault_routes

