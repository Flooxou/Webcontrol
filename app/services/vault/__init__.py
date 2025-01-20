# services/__init__.py

import hvac

# Configuration globale du client Vault
vault_client = hvac.Client(
    url="https://127.0.0.1:8200",
    token="VaultTokenToChange",
)

# Importation des fonctions
from .certificates import list_certificates, get_certificate_details
from .routes import vault_routes