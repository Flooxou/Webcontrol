from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    flash,
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


@vault_routes.app_context_processor
def inject_vault_servers():
    """Provide Vault servers and active selection to templates."""
    servers = VaultServer.query.all()
    selected_id = session.get('vault_id')
    active = VaultServer.query.get(selected_id) if selected_id else None
    return {
        'vault_servers': servers,
        'vault_selected_id': selected_id,
        'vault_active_server': active,
    }

@vault_routes.route('/admin')
def admin():
    """Render the Vault administration interface."""
    return render_template('vault/admin.html')


@vault_routes.route('/servers', methods=['GET', 'POST'])
def servers():
    """List and create Vault servers."""
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        token = request.form['token']
        server = VaultServer(name=name, address=address, token=token)
        db.session.add(server)
        db.session.commit()
        flash('Vault ajoute', 'success')
        return redirect(url_for('vault_routes.servers'))
    servers = VaultServer.query.all()
    selected_id = session.get('vault_id')
    return render_template('vault/servers.html', servers=servers, selected_id=selected_id)


@vault_routes.route('/servers/select', methods=['POST'])
def select_server():
    """Select the active Vault server."""
    server_id = int(request.form['vault_id'])
    server = VaultServer.query.get_or_404(server_id)
    session['vault_id'] = server.id
    configure_client(server.address, server.token)
    flash('Vault selectionne', 'success')
    return redirect(request.referrer or url_for('vault_routes.servers'))


@vault_routes.route('/servers/delete/<int:server_id>', methods=['POST'])
def delete_server(server_id):
    """Delete a Vault server."""
    server = VaultServer.query.get_or_404(server_id)
    db.session.delete(server)
    db.session.commit()
    flash('Vault supprime', 'success')
    return redirect(url_for('vault_routes.servers'))

@vault_routes.route('/issue_certificate', methods=['POST'])
def issue_certificate():
    """Issue a certificate from Vault using form fields."""
    if 'vault_id' not in session:
        flash('Veuillez s\u00e9lectionner un serveur Vault', 'warning')
        return redirect(url_for('vault_routes.servers'))
    path = request.form['path']
    role_name = request.form['role_name']
    common_name = request.form['common_name']
    alt_names = request.form['alt_names']
    ttl = request.form['ttl']
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
    """Show all certificates available in Vault."""
    if 'vault_id' not in session:
        flash('Veuillez s\u00e9lectionner un serveur Vault', 'warning')
        return redirect(url_for('vault_routes.servers'))
    certs = list_certificates()
    return render_template('vault/list_certificates.html', certs=certs)

@vault_routes.route('/certificate_details/<serial>', methods=['GET'])
def certificate_details(serial):
    """Display details for the certificate identified by ``serial``."""
    if 'vault_id' not in session:
        flash('Veuillez s\u00e9lectionner un serveur Vault', 'warning')
        return redirect(url_for('vault_routes.servers'))
    cert_details = get_certificate_details(serial)
    return render_template('vault/certificate_details.html', cert=cert_details)

