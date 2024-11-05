# helper script to add year and spotify-url

from tools import *

def get_id_and_url(artist, track, market):
    result = spotify_request(BASE_URL + 'search/?q=artist:' + artist + \
            ' track:' + track + '&type=track&market=' + market + '&limit=1')    
    return result['tracks']['items'][0]['id'], result['tracks']['items'][0]['external_urls']['spotify'] + '?si='

def get_year(track_id):
    # This is not neccessarily the year that you want! Make sure to
    # double check before you publish your PDF
    result = spotify_request(BASE_URL + 'tracks/' + track_id)
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