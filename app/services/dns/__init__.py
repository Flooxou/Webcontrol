DNS_SERVER = "127.0.0.1"

from .zones import create_zone, delete_zone
from .records import add_record, delete_record, list_records
from .routes import dns_routes