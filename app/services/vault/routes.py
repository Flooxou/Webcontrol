from flask import Blueprint, render_template, request, jsonify
from .certificates import list_certificates, get_certificate_details, create_certificate

vault_routes = Blueprint('vault_routes', __name__)

@vault_routes.route('/admin')
def admin():
    """Render the Vault administration interface."""
    return render_template('vault/admin.html')

@vault_routes.route('/issue_certificate', methods=['POST'])
def issue_certificate():
    """Issue a certificate from Vault using form fields."""
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
    certs = list_certificates()
    return render_template('vault/list_certificates.html', certs=certs)

@vault_routes.route('/certificate_details/<serial>', methods=['GET'])
def certificate_details(serial):
    """Display details for the certificate identified by ``serial``."""
    cert_details = get_certificate_details(serial)
    return render_template('vault/certificate_details.html', cert=cert_details)
