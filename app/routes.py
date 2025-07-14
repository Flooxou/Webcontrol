from flask import Blueprint, jsonify

# Création du blueprint principal
main_routes = Blueprint('main_routes', __name__)

# Exemple de route générale (page d'accueil)
@main_routes.route('/')
def home():
    """Simple health endpoint returning a JSON message."""
    return jsonify({"message": "Webcontrol API"})
