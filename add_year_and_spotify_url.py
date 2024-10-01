# helper script to add year and spotify-url

import requests

from functools import cache
from my_spotify_app import CLIENT_ID, CLIENT_SECRET

BASE_URL = 'https://api.spotify.com/v1/'
AUTH_URL = 'https://accounts.spotify.com/api/token'

def save_contents(filename, contents):
    with open(filename, 'w') as _file:
        _file.write(contents)

def get_contents(filename):
    with open(filename, 'r') as _file:
        contents = _file.readlines()
    return contents

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

def get_id_and_url(artist, track, market):
    result = _spotify_request(BASE_URL + 'search/?q=artist:' + artist + \
            ' track:' + track + '&type=track&market=' + market + '&limit=1')    
    return result['tracks']['items'][0]['id'], result['tracks']['items'][0]['external_urls']['spotify'] + '?si='

def get_year(track_id):
    # This is not neccessarily the year that you want! Make sure to
    # double check before you publish your PDF
    result = _spotify_request(BASE_URL + 'tracks/' + track_id)
    return result['album']['release_date'][:4]

def fix(contents, market):
    result = []
    for line in contents:
        title, artist = line.strip().split(';')
        try:
            track_id, url = get_id_and_url(artist, title, market)
            year = get_year(track_id)
        except Exception as e:
            raise(e)
            year, url = '', ''

        result.append('%s;%s;%s;%s\n' % (year, title, artist, url))
    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
                    prog = 'add_year_and_spotify_url.py',
                    description = 'Add year and Spotify URL in CSV file containing title and artist')
    parser.add_argument('filename')
    parser.add_argument('market')
    args = parser.parse_args()

    contents = fix(get_contents(args.filename), args.market)
    save_contents(args.filename, ''.join(contents))