from django.contrib import admin
from .models import Contador, Device, Leitura

@admin.register(Contador)
class ContadorAdmin(admin.ModelAdmin):
    list_display = ('serial','location','installation_date','active')
    search_fields = ('serial','location')

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name','api_key','contador','active','created_at')
    search_fields = ('name','api_key')

@admin.register(Leitura)
class LeituraAdmin(admin.ModelAdmin):
    list_display = ('contador','volume','captured_at','device','type','created_at')
    list_filter = ('type','created_at')
    search_fields = ('contador__serial','external_id')
