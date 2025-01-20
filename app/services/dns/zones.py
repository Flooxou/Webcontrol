def create_zone(zone_name, admin_email):
    """
    Crée une nouvelle zone DNS.

    :param zone_name: Nom de la zone DNS.
    :param admin_email: Email de l'administrateur de la zone.
    :return: Tuple (succès, message).
    """
    try:
        # Logique pour créer une zone DNS avec Bind9
        return True, f"Zone {zone_name} créée avec succès."
    except Exception as e:
        return False, str(e)

def delete_zone(zone_name):
    """
    Supprime une zone DNS existante.

    :param zone_name: Nom de la zone DNS.
    :return: Tuple (succès, message).
    """
    try:
        # Logique pour supprimer une zone DNS avec Bind9
        return True, f"Zone {zone_name} supprimée avec succès."
    except Exception as e:
        return False, str(e)
