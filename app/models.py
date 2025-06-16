from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance used across the application

db = SQLAlchemy()

class VaultServer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    token = db.Column(db.String(256), nullable=False)

