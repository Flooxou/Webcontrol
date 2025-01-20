from . import vault_client
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def extract_common_name(certificate_pem):
    """
    Extrait le nom commun (CN) d'un certificat PEM.

    :param certificate_pem: Le certificat au format PEM.
    :return: Le nom commun (CN) ou "Unknown" en cas d'erreur.
    """
    try:
        cert = x509.load_pem_x509_certificate(certificate_pem.encode(), default_backend())
        return cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
    except Exception:
        return "Unknown"

def list_certificates():
    """
    Récupère et traite la liste des certificats disponibles.

    :return: Liste des informations sur les certificats ou liste vide en cas d'erreur.
    """
    path = "pki/certs"
    try:
        response = vault_client.list(path)
        certs = response.get('data', {}).get('keys', [])
        cert_info = []
        for cert_serial in certs:
            cert_details = vault_client.read(f"pki/cert/{cert_serial}")
            if cert_details and 'data' in cert_details:
                certificate_pem = cert_details['data'].get('certificate', '')
                common_name = extract_common_name(certificate_pem)
                cert_info.append({"serial": cert_serial, "common_name": common_name})
        return cert_info
    except Exception as e:
        print(f"Error listing certificates: {str(e)}")
        return []

def get_certificate_details(serial):
    """
    Récupère les détails d'un certificat à partir de son numéro de série.

    :param serial: Numéro de série du certificat.
    :return: Détails du certificat ou dictionnaire vide en cas d'erreur.
    """
    try:
        cert_details = vault_client.read(f"pki/cert/{serial}")
        return cert_details.get('data', {})
    except Exception as e:
        print(f"Error retrieving certificate details: {str(e)}")
        return {}

def create_certificate(path, role_name, common_name, alt_names, ttl):
    response = vault_client.write(f"{path}/issue/{role_name}", common_name=common_name, alt_names=alt_names, ttl=ttl)
    
    return (response['data']['certificate'], response['data']['private_key'], "\n".join(response['data']['ca_chain']))