from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .zones import create_zone, delete_zone
from .records import add_record, delete_record, list_records

dns_routes = Blueprint('dns_routes', __name__)

@dns_routes.route('/admin')
def admin():
    """Render the DNS administration interface."""
    return render_template('dns/admin.html')

@dns_routes.route('/zones', methods=['POST'])
def create_zone_route():
    """Create a DNS zone from form parameters."""
    zone_name = request.form['zone_name']
    admin_email = request.form['admin_email']
    success, message = create_zone(zone_name, admin_email)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('dns_routes.admin'))

@dns_routes.route('/zones/<zone_name>', methods=['POST'])
def delete_zone_route(zone_name):
    """Delete the DNS zone specified in the URL."""
    success, message = delete_zone(zone_name)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('dns_routes.admin'))

@dns_routes.route('/records', methods=['POST'])
def add_record_route():
    """Add a DNS record based on form data."""
    zone_name = request.form['zone_name']
    record_name = request.form['record_name']
    record_type = request.form['record_type']
    record_value = request.form['record_value']
    ttl = request.form.get('ttl', 3600)
    
    try:
        response = add_record(zone_name, record_name, record_type, record_value, ttl)
        return jsonify({"message": "Enregistrement ajouté avec succès", "dns_response": str(response)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    success, message = add_record(zone_name, record_name, record_type, record_value, ttl)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('dns_routes.admin'))

@dns_routes.route('/records/<zone_name>/<record_name>', methods=['POST'])
def delete_record_route(zone_name, record_name):
    """Remove a DNS record from a given zone."""
    success, message = delete_record(zone_name, record_name)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('dns_routes.admin'))

@dns_routes.route('/records/<zone_name>', methods=['GET'])
def list_records_route(zone_name):
    """Display all DNS records for the given zone."""
    records = list_records(zone_name)
    return render_template('dns/list_records.html', zone_name=zone_name, records=records)
