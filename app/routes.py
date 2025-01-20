from flask import Blueprint, render_template

# Création du blueprint principal
main_routes = Blueprint('main_routes', __name__)

# Exemple de route générale (page d'accueil)
@main_routes.route('/')
def home():
    return render_template('index.html')