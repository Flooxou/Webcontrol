# Webcontrol

Webcontrol is a small Flask API that exposes endpoints to manage HashiCorp Vault
PKI certificates and basic DNS records. A separate front end is located in the
`frontend/` directory and can be served by any static web server.

## Installation

1. Clone the repository.
2. (Optional) Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the Python dependencies:
   ```bash
   pip install Flask hvac dnspython cryptography
   ```

## Environment Variables

The application can be configured with several environment variables:

- `FLASK_APP` – entry point of the application (use `run.py`).
- `FLASK_ENV` – set to `development` to enable debug mode.
- `SECRET_KEY` – secret key used by Flask. You can also edit `config.py` to
  change the default value.
- `VAULT_ADDR` and `VAULT_TOKEN` – Vault server address and token if you modify
  `app/services/vault/__init__.py` to read these values.
- `DNS_SERVER` – address of the DNS server. The value comes from the
  `DNS_SERVER` environment variable and defaults to `127.0.0.1` (see
  `app/services/dns/__init__.py`).
- `SQLALCHEMY_DATABASE_URI` – database connection string used by
  SQLAlchemy. If not set, the application stores data in a local
  SQLite file `webcontrol.db`.

## Running the Application

Start the web application using Flask's command line or run the script directly:

```bash
export FLASK_APP=run.py
export FLASK_ENV=development  # optional
flask run
```

Alternatively:

```bash
python run.py
```

The frontend in the `frontend/` directory is a static web interface. It can be
served by any static web server (for example `python -m http.server`) and will
interact with the API running on port 5000.

## Docker

The project provides Docker images for both the API and the web interface.
Start them together with the included PostgreSQL database:

```bash
docker compose up --build
```

The API will be available on <http://localhost:5000> and the frontend on
<http://localhost:8080>. Database files are persisted in the `db-data`
Docker volume.

## Docker

The project provides Docker images for both the API and the web interface.
Start them together with:

```bash
docker compose up --build
```

The API will be available on <http://localhost:5000> and the frontend on
<http://localhost:8080>.

## Offline Assets

Font Awesome styles are included in `frontend/static`.
