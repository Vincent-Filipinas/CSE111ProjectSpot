from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Token
from .util import *
from .Secret import *
from requests import Request, post


class AuthenticationURL(APIView):
    @staticmethod
    def get(self, request, format=None):
        scopes = 'user-read-currently-playing user-read-playback-state user-modify-playback-state'
        auth_url = Request('GET', SPOTIFY_AUTH_URL, params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': SPOTIFY_REDIRECT_URI,
            'client_id': SPOTIFY_CLIENT_ID
        }).prepare().url

        # auth_url = f'{SPOTIFY_AUTH_URL}client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={SPOTIFY_REDIRECT_URI}&scope=user-read-currently-playing'
        return HttpResponseRedirect(auth_url)


def callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    if error:
        return error

    response = post(SPOTIFY_TOKEN_URL, data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    token_type = response.get('token_type')

    auth_key = request.session.session_key

    if not request.session.exists(auth_key):
        request.session.create()
        auth_key = request.session.session_key

    create_or_update_tokens(
        session_id=auth_key,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=expires_in,
        token_type=token_type
    )

    # Create a redirect url to info
    redirect_url = f'http://127.0.0.1:8000/api/current-song?key={auth_key}'
    return HttpResponseRedirect(redirect_url)


class CheckAuthentication(APIView):
    def get(self, request, format=None):
        key = self.request.session.session_key

        if not self.request.session.exists(key):
            self.request.session.create()
            key = self.request.session.session_key

        auth_status = is_spotify_authenticated(key)

        if auth_status:
            redirect_url = f'http://127.0.0.1:8000/api/current-song?key={key}'
            return HttpResponseRedirect(redirect_url)
        else:
            # Will redirect us to authentication url
            redirect_url = 'http://127.0.0.1:8000/api/auth-url'
            return HttpResponseRedirect(redirect_url)


class CurrentSong(APIView):
    kwarg = "key"

    def get(self, request, format=None):
        key = request.GET.get(self.kwarg)
        print(key)
        token = Token.objects.filter(user=key)
        print(token)

        # Create an endpoint
        endpoint = 'player/currently-playing'
        response = spotify_request_exec(key, endpoint)

        if "error" in response or "item" not in response:
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        item = response.get('item')
        progress = response.get('progress_ms')
        is_playing = response.get('is_playing')
        duration = item.get('duration_ms')
        song_id = item.get('id')
        title = item.get('name')
        album_cover = item.get('album').get('images')[0].get('url')

        artists = ''

        for i, artist in enumerate(item.get('artists')):
            if i > 0:
                artists += ', '
            name = artist.get('name')
            artists += name

        song = {
            'id': song_id,
            'title': title,
            'artist': artists,
            'duration': duration,
            'time': progress,
            'album_cover': album_cover,
            'is_playing': is_playing,
        }

        return Response(song, status=status.HTTP_200_OK)
