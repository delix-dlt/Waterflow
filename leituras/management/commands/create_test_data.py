from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from leituras.models import Contador, Device
import secrets

User = get_user_model()

class Command(BaseCommand):
    help = 'Cria dados de teste: um contador e um device com api_key impresso'

    def handle(self, *args, **options):
        # cria superuser se não existir
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Superuser admin criado (senha: admin123)'))

        contador, created = Contador.objects.get_or_create(
            serial='CNT-0001',
            defaults={'location':'Bairro Central', 'installation_date': timezone.now().date(), 'active': True}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Contador {contador.serial} criado'))
        else:
            self.stdout.write(self.style.WARNING(f'Contador {contador.serial} já existe'))

        api_key = secrets.token_hex(20)  # 40 chars hex
        device, dcreated = Device.objects.get_or_create(
            name='ESP-001', contador=contador,
            defaults={'api_key': api_key, 'active': True}
        )
        # se já existia, mostramos a chave existente, senão a nova
        if not dcreated:
            api_key = device.api_key

        self.stdout.write(self.style.SUCCESS(f'Device criado: name={device.name} api_key={api_key}'))
        self.stdout.write(self.style.SUCCESS('Pronto. Agora podes usar o api_key acima no Postman.'))
