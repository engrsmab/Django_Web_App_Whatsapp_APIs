web: gunicorn device.wsgi
worker: python manage.py bot
scheduler: celery -A device worker --beat --scheduler django --loglevel=info