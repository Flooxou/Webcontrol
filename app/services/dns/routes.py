from flask import Blueprint, request, jsonify
from .zones import create_zone, delete_zone
from .records import add_record, delete_record, list_records

dns_routes = Blueprint('dns_routes', __name__)

@dns_routes.route('/admin')
def admin():
    """Simple message for DNS administration."""
    return jsonify({"message": "DNS administration"})

@dns_routes.route('/zones', methods=['POST'])
def create_zone_route():
    """Create a DNS zone from JSON payload."""
    data = request.get_json(silent=True) or request.form
    zone_name = data.get('zone_name')
    admin_email = data.get('admin_email')
    success, message = create_zone(zone_name, admin_email)
    status = 'success' if success else 'error'
    return jsonify({"status": status, "message": message})

@dns_routes.route('/zones/<zone_name>', methods=['DELETE', 'POST'])
def delete_zone_route(zone_name):
    """Delete the DNS zone specified in the URL."""
    success, message = delete_zone(zone_name)
    status = 'success' if success else 'error'
    return jsonify({"status": status, "message": message})

@dns_routes.route('/records', methods=['POST'])
def add_record_route():
    """Add a DNS record based on JSON data."""
    data = request.get_json(silent=True) or request.form
    zone_name = data.get('zone_name')
    record_name = data.get('record_name')
    record_type = data.get('record_type')
    record_value = data.get('record_value')
    ttl = data.get('ttl', 3600)
    
    try:
        response = add_record(zone_name, record_name, record_type, record_value, ttl)
        return jsonify({"message": "Enregistrement ajouté avec succès", "dns_response": str(response)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dns_routes.route('/records/<zone_name>/<record_name>', methods=['DELETE', 'POST'])
def delete_record_route(zone_name, record_name):
    """Remove a DNS record from a given zone."""
    success, message = delete_record(zone_name, record_name)
    status = 'success' if success else 'error'
    return jsonify({"status": status, "message": message})

@dns_routes.route('/records/<zone_name>', methods=['GET'])
def list_records_route(zone_name):
    """Return all DNS records for the given zone."""
    records = list_records(zone_name)
    return jsonify(records)
