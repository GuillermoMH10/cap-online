import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Crea o actualiza el superusuario inicial usando variables de entorno."

    def handle(self, *args, **options):
        username = os.environ.get("ADMIN_USERNAME", "admin").strip()
        email = os.environ.get("ADMIN_EMAIL", "admin@cap.com").strip()
        password = os.environ.get("ADMIN_PASSWORD", "")

        if not password:
            raise CommandError("Define ADMIN_PASSWORD antes de ejecutar este comando.")
        if len(password) < 8:
            raise CommandError("ADMIN_PASSWORD debe tener al menos 8 caracteres.")

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        action = "creado" if created else "actualizado"
        self.stdout.write(self.style.SUCCESS(f"Superusuario '{username}' {action} correctamente."))
