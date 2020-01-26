from django.contrib import admin
from .models import Host, Session, RequestedSong, Adjective, Animal
# Register your models here.
@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ('user', 'spotify_token', 'refresh_token')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('host',)

@admin.register(RequestedSong)
class RequestedSongAdmin(admin.ModelAdmin):
    list_display = ('session', 'uri', 'name')

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Adjective)
class AdjectiveAdmin(admin.ModelAdmin):
    list_display = ('name',)
