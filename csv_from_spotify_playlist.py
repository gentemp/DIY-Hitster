# helper script to add year and spotify-url

import requests

from functools import cache
from credentials.spotify import CLIENT_ID, CLIENT_SECRET

BASE_URL = 'https://api.spotify.com/v1/'
AUTH_URL = 'https://accounts.spotify.com/api/token'

@cache
def get_access_token(id, secret):
    auth_response = requests.post(AUTH_URL,
    {   
        'grant_type': 'client_credentials',
        'client_id': id,
        'client_secret': secret
    })
    auth_response_data = auth_response.json()
    return auth_response_data['access_token']

def _spotify_request(request):
    headers = { 'Authorization':
                'Bearer {token}'.format(token = get_access_token(CLIENT_ID, CLIENT_SECRET)) }
    return requests.get(request, headers = headers).json()

def get_playlist_contents(playlist):
    result = []
    tracks = _spotify_request(BASE_URL + 'playlists/' + playlist + '/tracks')    
    for item in tracks['items']:
        result.append(item['track']['artists'][0]['name'] + ' - ' + item['track']['name'])
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
                    prog = 'csv_from_spotify_playlist.py',
                    description = 'Create a CSV file from a Spotify playlist')
    args = parser.parse_args()

    contents = get_playlist_contents('5wFZD9H6yDAUSHACTFAugC')
    print(contents)