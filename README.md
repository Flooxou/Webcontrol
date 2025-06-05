# Webcontrol

Webcontrol is a small Flask application that provides a web interface for managing
HashiCorp Vault PKI certificates and basic DNS records. The project bundles a few
HTML templates with minimal JavaScript and CSS.

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

## Offline Assets

Font Awesome styles are included in
`static/css/font-awesome_6.5.0_all.min.css`. To run the interface without
internet access, download the matching Font Awesome 6.5.0 package and copy its
`webfonts` directory into `static/webfonts/`.
