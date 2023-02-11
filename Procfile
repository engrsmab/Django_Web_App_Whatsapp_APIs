web: gunicorn device.wsgi
scheduler: celery -A device worker --beat --scheduler django --loglevel=info
worker: python manage.py bot
