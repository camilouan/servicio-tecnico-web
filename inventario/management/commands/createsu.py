from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Crear superusuario automaticamente'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = "admin"
        email = "admin@admin.com"
        password = "admin123"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS("Superusuario creado"))
        else:
            self.stdout.write("El superusuario ya existe")