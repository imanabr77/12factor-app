web: gunicorn app:create_app()
worker: celery -A tasks worker --loglevel=info
release: python manage.py migrate