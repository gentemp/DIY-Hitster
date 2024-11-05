# helper script to create a csv file from a spotify playlist

from tools import *

def get_data(track_id):
    result = ''
    data = spotify_request(BASE_URL + 'tracks/' + track_id)
    result += data['album']['release_date'][:4] + ';'
    result += ', '.join([artist['name'] for artist in data['artists']]) + ';'
    result += data['name'] + ';'
    result += data['external_urls']['spotify'] + '?si='

    return result

def get_playlist_contents(playlist):
    result = []
    tracks = spotify_request(BASE_URL + 'playlists/' + playlist + '/tracks')
    while True: 
        for item in tracks['items']:
            track_id = item['track']['id']
            result.append(get_data(track_id))
        
        if tracks['next']:
            tracks = spotify_request(tracks['next'])
        else:
            break

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