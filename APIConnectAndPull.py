# -*- coding: utf-8 -*-
"""
Spotify API Connection
"""

import requests
import base64, json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os

import sys
sys.executable

#Getting Access Token
authUrl = "https://accounts.spotify.com/api/token"
authHeader = {}
authData = {}

def getAccessToken(clientID, clientSecret):
    message = f"{clientID}:{clientSecret}"
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    
    authHeader['Authorization'] = "Basic " + base64_message
    authData['grant_type'] = "client_credentials"
    r = requests.post(authUrl, headers = authHeader, data=authData)
    
    r_object = r.json()
    
    accessToken = r_object['access_token']
    
    return accessToken

cid = 'a8553eb77f284c2e8e0319757d58f652'
secret = 'be9f7174585c45d49a6d67fda9a4caea'
token = getAccessToken(cid, secret)

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) #Used to connect to Spotipy
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager) #Used for acquiring audio features

#Pulling names and IDs for each season-themed playlist
def getPlaylists(token, UserID):
    userEndpoint = f"https://api.spotify.com/v1/users/{UserID}/playlists/?offset=0&limit=50"
    getHeader = {"Authorization": "Bearer " + token}
    r = requests.get(userEndpoint, headers=getHeader)
    playlistObject = r.json()
    return playlistObject

playlist_list = getPlaylists(token, 'brandon596')

for p in playlist_list['items']:
    print(p['name'])

playlist_names = []
playlist_ids = []
for p in playlist_list['items']:
    prefixes = ['Spring', 'Winter', 'Summer', 'Fall'] 
    if p['name'].startswith(tuple(prefixes)):
        playlist_names.append(p['name'])
        playlist_ids.append(p['id'])
playlists = pd.DataFrame({'Name': playlist_names, 'ID': playlist_ids})

#Missing Winter 2018-2019 and Spring 2019

#Looping through each playlist and collecting the following information:
    #Playlist Name
    #Track URI
    #Track Name
    #Track Artist
    #Track Album

def getPlaylistTracks(token, playlistID):
    playlistEndpoint = f"https://api.spotify.com/v1/playlists/{playlistID}"
    getHeader = {"Authorization": "Bearer " + token}
    r = requests.get(playlistEndpoint, headers=getHeader)
    playlistObject = r.json()
    return playlistObject

df_full = pd.DataFrame()
for i in playlists['ID']:
    tracklist = getPlaylistTracks(token, i)
    uri_list = []
    name_list = []
    artist_list = []
    album_list = []
    for t in tracklist['tracks']['items']:
        uri_list.append(t['track']['uri'])
        name_list.append(t['track']['name'])
        artist_list.append(t['track']['artists'][0]['name'])
        album_list.append(t['track']['album']['name'])
    df = pd.DataFrame({'Playlist ID': i, 'Song URI': uri_list, 'Song Name': name_list,
                       'Artist': artist_list, 'Album': album_list})
    df_full = df_full.append(df)
    
#Merging in Playlist Name
df_full = df_full.merge(playlists, how='left', left_on='Playlist ID', right_on='ID')
df_full = df_full.rename(columns = {'Name': 'Playlist Name'})
df_full = df_full[['Playlist Name', 'Song URI', 'Song Name', 'Artist', 'Album']]        
        
    
#Extracting Audio Features for each song and merging into final dataset
audio_df_full = pd.DataFrame()
for i in df_full['Song URI']:
    audio_df = pd.DataFrame(sp.audio_features(i)[0], index=[0])
    audio_df_full = audio_df_full.append(audio_df)

df_full = df_full.merge(audio_df_full, how='left', left_on='Song URI', right_on='uri')
df_full.columns = df_full.columns.str.title()

#Parsing out dates and organizing by time
df_full['Season'] = df_full['Playlist Name'].str.split(' ').str[0]
df_full['Year'] = df_full['Playlist Name'].str.split(' ').str[1]

df_final = df_full[['Playlist Name', 'Song Uri', 'Song Name', 'Artist', 'Album',
                   'Danceability', 'Energy', 'Key', 'Loudness', 'Mode', 'Speechiness',
                   'Acousticness', 'Instrumentalness', 'Liveness', 'Valence', 'Tempo',
                   'Duration_Ms', 'Time_Signature']]


#Exporting Dataset (Will use for EDA/Clustering)
df_final.to_excel('Sotify DS Project/Data/playlist_data.xlsx', index=False)
