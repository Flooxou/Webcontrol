from flask import Flask
from app.routes import main_routes  # Import du blueprint principal
from app.services.vault import vault_routes
from app.services.dns import dns_routes

def create_app():
    app = Flask("Webcontrol")
    app.config.from_object('config.Config')
    
    with app.app_context():
        # Import routes
        app.register_blueprint(vault_routes, url_prefix='/vault')
        app.register_blueprint(dns_routes, url_prefix='/dns')
        app.register_blueprint(main_routes)  # Pas de préfixe pour les routes principales
    return app