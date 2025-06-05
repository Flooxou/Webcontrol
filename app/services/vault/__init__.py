# services/__init__.py

import os
import hvac

# Configuration globale du client Vault
VAULT_URL = os.environ.get("VAULT_URL", "https://127.0.0.1:8200")
VAULT_TOKEN = os.environ.get("VAULT_TOKEN", "VaultTokenToChange")

vault_client = hvac.Client(url=VAULT_URL, token=VAULT_TOKEN)

# Importation des fonctions
from .certificates import list_certificates, get_certificate_details
from .routes import vault_routes
