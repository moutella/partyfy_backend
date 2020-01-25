import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import requests
from decouple import config
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import authenticate, login, logout
from .models import Host
# Create your views here.

class Login(View):
    def get(self, request):
        scope = 'streaming user-read-currently-playing user-read-playback-state user-modify-playback-state'

        redirect_url = request.build_absolute_uri('/')[:-1].strip("/")  +reverse('login_return')
        print(redirect_url)
        client_id=config("SPOTIFY_CLIENT_ID")
        spotify_string = 'https://accounts.spotify.com/authorize?client_id={}&response_type=code&redirect_uri={}&scope={}'
        spotify_string = spotify_string.format(client_id, redirect_url, scope)
        context = {
            'login_href' : spotify_string
        }
        return render(request, 'login.html', context)

class LoginReturnPage(View):
    def get(self, request):
        code = request.GET['code']
        redirect_url = request.build_absolute_uri('/')[:-1].strip("/")  +reverse('login_return')
        spotify_auth = SpotifyOAuth(
            client_id=config('SPOTIFY_CLIENT_ID'),
            client_secret=config('SPOTIFY_SECRET'),
            redirect_uri=redirect_url
        )
        token = spotify_auth.get_access_token(code)
        sp = spotipy.Spotify(auth=token['access_token'])
        spotify_info = sp.me()
        print(spotify_info['id'])
        try:
            user = User.objects.get(username=spotify_info['id'])
            host = Host.objects.get(user=user)
            host.spotify_token = token['access_token']
            host.refresh_token = token['refresh_token']
            host.save()
            login(request, user)
            return HttpResponse("Já existia e logou")
        except:
            user = User(username=spotify_info['id'], first_name=spotify_info['display_name'])
            user.save()
            host = Host(
                user=user,
                spotify_token = token['access_token'],
                refresh_token = token['refresh_token']
            )
            host.save()
            login(request, user)
            return HttpResponse("Novo usuário logou")
        