"""
Gunicorn configuration file.

This configuration file sets up the Gunicorn server with environment variables
loaded from a .env file. The following settings are configured:

- workers: Number of worker processes for handling requests. Default is 2.
- threads: Number of threads per worker process. Default is 4.
- bind: The socket to bind. Default is '0.0.0.0:8080'.
- forwarded_allow_ips: IPs from which the server will accept forwarded requests. Default is '*'.
- secure_scheme_headers: Headers to mark requests secure. Default is {'X-Forwarded-Proto': 'https'}.

Environment Variables:
- GUNICORN_PROCESSES: Number of worker processes.
- GUNICORN_THREADS: Number of threads per worker process.
- GUNICORN_BIND: The socket to bind.
"""
import os
from dotenv import load_dotenv

load_dotenv()

workers = int(os.getenv('GUNICORN_PROCESSES', '2'))

threads = int(os.getenv('GUNICORN_THREADS', '4'))

# timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))

bind = os.getenv('GUNICORN_BIND', '0.0.0.0:8080')

FORWARD_ALLOW_IPS = '*'

secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }
