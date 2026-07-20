"""
WSGI config for cap_online project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cap_online.settings')

# ──────────────────────────────────────────────────────────────
# Auto-setup: corre migrate y collectstatic al iniciar el servidor
# Esto garantiza que funcione en Render sin importar el Build/Start Command
# ──────────────────────────────────────────────────────────────
def _auto_setup():
    try:
        import django
        django.setup()
        from django.core.management import call_command

        print("[wsgi] Ejecutando migraciones...", flush=True)
        call_command('migrate', '--no-input', verbosity=1)
        print("[wsgi] Migraciones completadas.", flush=True)

        print("[wsgi] Recopilando archivos estáticos...", flush=True)
        call_command('collectstatic', '--no-input', verbosity=0)
        print("[wsgi] Archivos estáticos listos.", flush=True)

    except Exception as exc:
        print(f"[wsgi] Error en auto-setup: {exc}", file=sys.stderr, flush=True)

_auto_setup()

application = get_wsgi_application()
