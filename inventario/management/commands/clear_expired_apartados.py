from django.core.management.base import BaseCommand
from inventario.models import Apartado


class Command(BaseCommand):
    help = 'Libera apartados vencidos y devuelve stock al producto (ejecutar desde un cron)'

    def handle(self, *args, **options):
        updated = Apartado.actualizar_apartados_vencidos()
        self.stdout.write(self.style.SUCCESS(f'Apartados actualizados: {updated}'))
