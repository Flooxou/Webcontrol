from flask import Flask
from flask_cors import CORS
from app.routes import main_routes
from app.services.vault import vault_routes
from app.services.dns import dns_routes
from .models import db


def create_app():
    app = Flask("Webcontrol")
    CORS(app)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        app.register_blueprint(vault_routes, url_prefix='/vault')
        app.register_blueprint(dns_routes, url_prefix='/dns')
        app.register_blueprint(main_routes)
        db.create_all()
    return app

