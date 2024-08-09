import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


cid ='xxxx' #number of x is not equal to the number of characters in the id
secret ='xxxx'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def main():

    artist_name='Your Favorite Artist'
    album_name='the spotify url of the album'
    basic_data=get_album_tracks(album_name)
    song_data=get_track_info(basic_data)
    spotify_data=merge_frames(basic_data,song_data)
    song_popularity=popularity(spotify_data)
    harr_song_data=merge_frames(spotify_data,song_popularity)
    harr_song_data=harr_song_data.drop('uri',axis=1)
    write_to_csv(harr_song_data,'filename (no need of csv extension)')



def get_album_tracks(uri_info):
    uri = []
    track = []
    duration = []
    explicit = []
    track_number = []
    one = sp.album_tracks(uri_info, limit=50, offset=0, market='US')
    df1 = pd.DataFrame(one)
    
    for i, x in df1['items'].items():
        uri.append(x['uri'])
        track.append(x['name'])
        duration.append(x['duration_ms'])
        explicit.append(x['explicit'])
        track_number.append(x['track_number'])
    
    df2 = pd.DataFrame({
    'uri':uri,
    'track':track,
    'duration_ms':duration,
    'explicit':explicit,
    'track_number':track_number})
    
    return df2


def get_track_info(df):
    danceability = []
    energy = []
    key = []
    loudness = []
    speechiness = []
    acousticness = []
    instrumentalness = []
    liveness = []
    valence = []
    tempo = []
    for i in df['uri']:
        for x in sp.audio_features(tracks=[i]):
            danceability.append(x['danceability'])
            energy.append(x['energy'])
            key.append(x['key'])
            loudness.append(x['loudness'])
            speechiness.append(x['speechiness'])
            acousticness.append(x['acousticness'])
            instrumentalness.append(x['instrumentalness'])
            liveness.append(x['liveness'])
            valence.append(x['valence'])
            tempo.append(x['tempo'])
            
    df2 = pd.DataFrame({
    'danceability':danceability,
    'energy':energy,
    'key':key,
    'loudness':loudness,
    'speechiness':speechiness,
    'acousticness':acousticness,
    'instrumentalness':instrumentalness,
    'liveness':liveness,
    'valence':valence,
    'tempo':tempo})
    
    return df2

def merge_frames(df1, df2):
    df3 = df1.merge(df2, left_index= True, right_index= True)
    return df3



def popularity(df):
    empty = []
    for i in df['uri']:
            series_track = pd.Series(sp.track(i)['popularity'])
            empty.append(series_track)
    df2 = pd.DataFrame(empty)
    df2.columns=['popularity']
    return df2
def write_to_csv(df,filename):
    df.to_csv(f'{filename}.csv',index=False)


if __name__=='__main__':
    main()
