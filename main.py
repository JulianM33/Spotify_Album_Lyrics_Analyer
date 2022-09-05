from os import name

import pandas as pd

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from lyrics import scrape_lyrics

cid = 'b92ebc1168e14bb3b37fbbc97da39ce1'
secret = '41ec15d424784166b81326c38b533dc4'
token = 'BQBAP2ezZ3zCMPEbwYNVVUHbTFC0VPqDtHMGylC9Wtxi0SKHTDbhBWWIfIlkfRBYmXr8LrL5S57yPnLYyTxY8YW3isW5e_lwchnjpqaZ3R6Q-wBIGIN0MEcITsKdGpZff121NHA50d5dn-Ppo0J5aBQYFLJRzer5rUu6hPdESqqRqMBG0gfbFLL_XXNvqneDdz4'

blonde = 'https://open.spotify.com/album/5zBPRXCAc801vyHWoRurNZ?si=zvP1k1YZR-WKNAYYA-IPvga'
album = 'https://open.spotify.com/album/2eTxZYoqIv4MoLqwh73qvo?si=G6gccpA-TImlLEO4DmY5dg'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


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
        'uri': uri,
        'track': track,
        'duration_ms': duration,
        'explicit': explicit,
        'track_number': track_number})

    return df2

# function to attach lyrics onto data frame
# artist_name should be inserted as a string
def lyrics_onto_frame(df1, artist_name):
    for i, x in enumerate(df1['track']):
        test = scrape_lyrics(artist_name, x)
        df1.loc[i, 'lyrics'] = test
    return df1


print("hello")
df = get_album_tracks(album)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)

l_df = lyrics_onto_frame(df, "Beach-house")
print(l_df)
print("break")



#    print(df)
#    print(df.items)
