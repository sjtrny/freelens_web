import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Setup the superuser"

    def handle(self, *args, **kwargs):
        username = (
            os.environ["DJANGO_SUPERUSER_USERNAME"]
            if "DJANGO_SUPERUSER_USERNAME" in os.environ
            else "admin"
        )
        email = (
            os.environ["DJANGO_SUPERUSER_EMAIL"]
            if "DJANGO_SUPERUSER_EMAIL" in os.environ
            else "admin@example.com"
        )
        password = (
            os.environ["DJANGO_SUPERUSER_PASSWORD"]
            if "DJANGO_SUPERUSER_PASSWORD" in os.environ
            else "password"
        )

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username, email=email, password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f"Superuser '{username}' created successfully.")
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"Superuser '{username}' already exists - skipping ."
                )
            )
