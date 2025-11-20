from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Contador(models.Model):
    serial = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    location = models.CharField(max_length=255, null=True, blank=True)
    installation_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.serial

class Device(models.Model):
    name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=64, unique=True)
    contador = models.ForeignKey(Contador, null=True, blank=True, on_delete=models.SET_NULL, related_name='device')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.api_key[:8]})"

class Leitura(models.Model):
    TIPOS = [('automatic', 'automatic'), ('manual', 'manual')]

    contador = models.ForeignKey(Contador, on_delete=models.CASCADE, related_name='leituras')
    device = models.ForeignKey(Device, null=True, blank=True, on_delete=models.SET_NULL, related_name='leituras')
    volume = models.DecimalField(max_digits=12, decimal_places=3)
    flow_rate = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    captured_at = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=TIPOS, default='automatic')
    external_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['contador','captured_at']),
        ]
        # opcional: evitar duplicados por device+external_id (descomentar quando quiseres)
        # constraints = [
        #     models.UniqueConstraint(fields=['device','external_id'], name='unique_device_external')
        # ]

    def __str__(self):
        return f"{self.contador.serial} - {self.volume} @ {self.captured_at or self.created_at}"
