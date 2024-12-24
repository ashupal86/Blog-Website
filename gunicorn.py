# gunicorn_config.py
bind = "0.0.0.0:8000"
workers = 4
threads = 2
worker_class = "gthread"
preload_app = True
timeout = 120
max_requests = 1000
max_requests_jitter = 50
accesslog = "access.log"
errorlog = "error.log"
loglevel = "info"
