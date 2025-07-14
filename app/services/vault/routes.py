from flask import (
    Blueprint,
    request,
    jsonify,
    session,
)

from .certificates import list_certificates, get_certificate_details, create_certificate
from app.models import db, VaultServer
from . import configure_client

vault_routes = Blueprint('vault_routes', __name__)


@vault_routes.before_request
def load_active_vault():
    """Configure the Vault client from the selected server if available."""
    server_id = session.get('vault_id')
    if server_id:
        server = VaultServer.query.get(server_id)
        if server:
            configure_client(server.address, server.token)


# API does not use template context processors

@vault_routes.route('/admin')
def admin():
    """Return a simple message for the admin endpoint."""
    return jsonify({"message": "Vault administration"})


@vault_routes.route('/servers', methods=['GET', 'POST'])
def servers():
    """List and create Vault servers."""
    if request.method == 'POST':
        data = request.get_json() or {}
        server = VaultServer(
            name=data.get('name'),
            address=data.get('address'),
            token=data.get('token'),
        )
        db.session.add(server)
        db.session.commit()
        return jsonify({"id": server.id, "name": server.name, "address": server.address}), 201

    servers = VaultServer.query.all()
    result = [{"id": s.id, "name": s.name, "address": s.address} for s in servers]
    return jsonify(result)


@vault_routes.route('/servers/select', methods=['POST'])
def select_server():
    """Select the active Vault server."""
    data = request.get_json() or {}
    server_id = int(data.get('vault_id'))
    server = VaultServer.query.get_or_404(server_id)
    session['vault_id'] = server.id
    configure_client(server.address, server.token)
    return jsonify({"status": "selected", "server_id": server.id})


@vault_routes.route('/servers/<int:server_id>', methods=['DELETE'])
def delete_server(server_id):
    """Delete a Vault server."""
    server = VaultServer.query.get_or_404(server_id)
    db.session.delete(server)
    db.session.commit()
    return jsonify({"status": "deleted"})

@vault_routes.route('/issue_certificate', methods=['POST'])
def issue_certificate():
    """Issue a certificate from Vault using form fields."""
    if 'vault_id' not in session:
        return jsonify({"error": "Vault server not selected"}), 400
    data = request.get_json() or {}
    path = data.get('path')
    role_name = data.get('role_name')
    common_name = data.get('common_name')
    alt_names = data.get('alt_names')
    ttl = data.get('ttl')
    try:
        certificate, private_key, ca_chain = create_certificate(path, role_name, common_name, alt_names, ttl)
        
        return jsonify({
            "status": "success",
            "certificate": certificate,
            "private_key": private_key,
            "ca_chain": ca_chain
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@vault_routes.route('/list_certificates')
def list_certificates_route():
    """Return all certificates available in Vault."""
    if 'vault_id' not in session:
        return jsonify({"error": "Vault server not selected"}), 400
    certs = list_certificates()
    return jsonify(certs)

@vault_routes.route('/certificate_details/<serial>', methods=['GET'])
def certificate_details(serial):
    """Return details for the certificate identified by ``serial``."""
    if 'vault_id' not in session:
        return jsonify({"error": "Vault server not selected"}), 400
    cert_details = get_certificate_details(serial)
    return jsonify(cert_details)

