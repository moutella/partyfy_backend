from django.contrib import admin
from .models import Host
# Register your models here.
@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ('user', 'spotify_token', 'refresh_token')

