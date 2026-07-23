web: sh -c 'if [ -n "$ADMIN_PASSWORD" ]; then python manage.py crear_admin; fi; exec gunicorn cap_online.wsgi:application --bind 0.0.0.0:${PORT:-10000}'
