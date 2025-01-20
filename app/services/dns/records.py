from flask import jsonify
import dns.query
import dns.update
from . import DNS_SERVER

def add_record(zone_name, record_name, record_type, record_value, ttl=3600):
    """
    Ajoute un enregistrement DNS dans une zone.

    :param zone_name: Nom de la zone DNS.
    :param record_name: Nom de l'enregistrement.
    :param record_type: Type d'enregistrement (e.g., A, CNAME).
    :param record_value: Valeur de l'enregistrement (e.g., IP ou domaine).
    :param ttl: Durée de vie en secondes (par défaut : 3600).
    :return: Tuple (succès, message).
    """
    update = dns.update.Update(zone_name)
    update.add(f"{record_name}.{zone_name}.", ttl, record_type, record_value)
    response = dns.query.tcp(update, DNS_SERVER)
    return response

def delete_record(zone_name, record_name):
    """
    Supprime un enregistrement DNS d'une zone.

    :param zone_name: Nom de la zone DNS.
    :param record_name: Nom de l'enregistrement à supprimer.
    :return: Tuple (succès, message).
    """
    try:
        # Logique pour supprimer un enregistrement DNS avec Bind9
        return True, f"Enregistrement {record_name} supprimé de la zone {zone_name}."
    except Exception as e:
        return False, str(e)

def list_records(zone_name):
    """
    Liste tous les enregistrements d'une zone DNS.

    :param zone_name: Nom de la zone DNS.
    :return: Liste des enregistrements ou liste vide en cas d'erreur.
    """
    try:
        # Logique pour lister les enregistrements DNS dans une zone
        return [
            {"name": "example.com", "type": "A", "value": "192.168.1.1", "ttl": 3600},
            {"name": "www.example.com", "type": "CNAME", "value": "example.com", "ttl": 3600},
        ]
    except Exception as e:
        return []
