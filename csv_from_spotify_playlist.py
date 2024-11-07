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

def get_playlist_contents(playlist, backup):
    _backup_dict = {}
    if backup:
        for line in backup:
            _, _, _, url = line.split(';')
            # extract the id part from the url
            # https://open.spotify.com/track/ 28ihA2Fp5zRmcmi8hpfWiC ?si=
            id = url[31:-5]
            _backup_dict[id] = line.strip()

    result = []
    tracks = spotify_request(BASE_URL + 'playlists/' + playlist + '/tracks')
    while True: 
        for item in tracks['items']:
            track_id = item['track']['id']
            try:
                result.append(_backup_dict[track_id])
            except KeyError:
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

    # reuse existing rows in order to both speed up the script execution
    # and to keep manually fixed values
    backup = None
    try:
        backup = get_contents(args.filename)
    except FileNotFoundError:
        pass
    contents = get_playlist_contents(args.playlist, backup)
    save_contents(args.filename, '\n'.join(contents))