# helper script to add year and spotify-url

import requests

from functools import cache
from credentials.spotify import CLIENT_ID, CLIENT_SECRET

BASE_URL = 'https://api.spotify.com/v1/'
AUTH_URL = 'https://accounts.spotify.com/api/token'

def save_contents(filename, contents):
    with open(filename, 'w') as _file:
        _file.write(contents)

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

def get_data(track_id):
    result = ''
    data = _spotify_request(BASE_URL + 'tracks/' + track_id)
    result += data['album']['release_date'][:4] + ';'
    result += ', '.join([artist['name'] for artist in data['artists']]) + ';'
    result += data['name'] + ';'
    result += data['external_urls']['spotify'] + '?si='

    return result

def get_playlist_contents(playlist):
    result = []
    tracks = _spotify_request(BASE_URL + 'playlists/' + playlist + '/tracks')    
    for item in tracks['items']:
        track_id = item['track']['id']
        result.append(get_data(track_id))

    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
                    prog = 'csv_from_spotify_playlist.py',
                    description = 'Create a CSV file from a Spotify playlist')
    parser.add_argument('filename')
    parser.add_argument('playlist')
    args = parser.parse_args()

    contents = get_playlist_contents(args.playlist)
    save_contents(args.filename, '\n'.join(contents))