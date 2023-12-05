from django.http import JsonResponse
from .models import Token
from django.utils import timezone
from datetime import timedelta
from requests import post, get
from .Secret import *
import requests


# Check Token
def check_tokens(session_id):
    tokens = Token.objects.filter(user=session_id)
    if tokens:
        return tokens[0]
    else:
        return None


# Create and Update the Token Model
def create_or_update_tokens(session_id, access_token, refresh_token, expires_in, token_type):
    tokens = check_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds = expires_in)

    # Updates Tokens if they exist
    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])

    else:
        tokens = Token(
            user=session_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
            token_type=token_type
        )
        tokens.save()


# Check Authentication
def is_spotify_authenticated(session_id):
    tokens = check_tokens(session_id)

    if tokens:
        if tokens.expires_in <= timezone.now():
            refresh_token_func(session_id)
        return True
    return False


# Refresh token function
def refresh_token_func(session_id):
    refresh_token = check_tokens(session_id).refresh_token

    response = post(SPOTIFY_TOKEN_URL, data={
        'grant_type': "refresh_token",
        'refresh_token': refresh_token,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    }).json()

    access_token = response.get('access_token')
    expires_in = response.get('expires_in')
    token_type = response.get('token_type')

    create_or_update_tokens(
        session_id=session_id,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=expires_in,
        token_type=token_type
    )


def spotify_request_exec(session_id, endpoint):
    token = check_tokens(session_id)
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token.access_token}

    base_url = SPOTIFY_API_BASE_URL + 'me/'

    # Get data on the song from the Spotify API
    api_url = f'{base_url + endpoint}'
    response = requests.get(base_url + endpoint,{}, headers=headers)

    try:
        return response.json()
    except:
        return JsonResponse({'Error': 'Issue with request'})
