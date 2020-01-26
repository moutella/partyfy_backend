import traceback
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import requests
from decouple import config
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Host, Session, RequestedSong, Adjective, Animal
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
        animals = Animal.objects.all()
        adjs = Adjective.objects.all()
        try:
            user = User.objects.get(username=spotify_info['id'])
            host = Host.objects.get(user=user)
            host.spotify_token = token['access_token']
            host.refresh_token = token['refresh_token']
            host.save()
            login(request, user)
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
        
        new_session = False
        while not new_session:
            adj_1 = random.choice(adjs)
            adj_2 = random.choice(adjs)
            anim = random.choice(animals)   
            session_id = "{}{}{}".format(anim, adj_1, adj_2)
            host = Host.objects.get(user=request.user)
            try:
                session = Session.objects.get(session_id=session_id)
            except Session.DoesNotExist:
                session = Session(
                    session_id=session_id,
                    host=host
                )
                session.save()
                new_session = True    
        return HttpResponseRedirect(reverse('session', kwargs={'session_id':session_id}))
        
class SessionView(View):
    def get(self, request, session_id):
        session = Session.objects.get(session_id=session_id)
        token = session.host.spotify_token
        sp = spotipy.Spotify(auth=token)
        
        current = sp.currently_playing()
        
        context = {
            'session_id': session_id
        }
        try:
            current_song = RequestedSong.objects.get(uri=current['item']['uri'])
            session_songs_played = RequestedSong.objects.filter(created_at__lte=current_song.created_at)
            for song in session_songs_played:
                song.played=True
                song.save()
            
            already_playing = True
            session_songs = RequestedSong.objects.filter(
                session__session_id=session_id,
                created_at__gt=current_song.created_at
            )
            print(session_songs)
            context["songs"] = session_songs
            context["current_song"] = current['item']['name']
        except:
            traceback.print_exc()
        return render(request, 'session.html', context)

class MusicRequestView(View):
    def post(self, request):
        print(request.POST)
        session_id = request.POST['session_id']
        session = Session.objects.get(session_id=session_id)
        token = session.host.spotify_token
        sp = spotipy.Spotify(auth=token)
        
        current = sp.currently_playing()
        already_playing = False
        current_song = None
        track = sp.track(request.POST['song_uri'])
        print(track)
        try:
            current_song = RequestedSong.objects.get(uri=current['item']['uri'])
            already_playing = True
        except:
            pass
        try:
            new_request = RequestedSong.objects.get(
                session=session,
                song_id=track['id']
            )
            messages.error(request, "Música já está na fila")
        except RequestedSong.DoesNotExist:
            new_request = RequestedSong(
                session=session,
                uri=request.POST['song_uri'],
                name=track['name'],
                song_id=track['id']
            )
            new_request.save()
            try:
                session_songs = RequestedSong.objects.filter(session=session, played=False)
                if already_playing:
                    session_songs_played = session_songs.filter(created_at__lte=current_song.created_at)
                    session_songs = session_songs.filter(created_at__gt=current_song.created_at)
                    for song in session_songs_played:
                        song.played = True
                        song.save()
                if current:
                    songs_with_current = [current['item']['uri']]
                    for song in session_songs:
                        songs_with_current.append(song.uri)
                    current = sp.currently_playing()
                    progress = current['progress_ms']
                    print(songs_with_current)
                    sp.start_playback(uris=songs_with_current)
                    sp.seek_track(progress)
                else:
                    sp.start_playback(uris=songs)
            except Exception as e:
                traceback.print_exc()    
                messages.error(request, str(e))
        return HttpResponseRedirect(reverse('session', kwargs={'session_id':session_id}))

class CreateNewSession(View):
    def get(self, request):
        pass

class Home(View):
    def get(self, request):
        return render(request, 'index.html')