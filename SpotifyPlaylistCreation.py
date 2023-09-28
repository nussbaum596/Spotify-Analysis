# -*- coding: utf-8 -*-
"""
This program uses the K-Means clustering results to create new playlists with my collection of songs
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import pandas as pd
import os

os.chdir(r'C:/Users/BrandonN/OneDrive - InSightec/Insightec/Brandon/Spotify DS Project')

cid = 'a8553eb77f284c2e8e0319757d58f652'
secret = 'be9f7174585c45d49a6d67fda9a4caea'
redirect_uri = 'http://localhost:8888'

scope = 'playlist-modify-public'
username = 'brandon596'

token = SpotifyOAuth(scope = scope, 
                     username=username,
                     SPOTIPY_CLIENT_ID = cid
                     )

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) #Used to connect to Spotipy
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager) #Used for acquiring audio features

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


token = getAccessToken(cid, secret)





df = pd.read_excel('Data/playlist_data_withclusters.xlsx')

sp.user_playlist_create('cid', 'Test', public=True, collaborative=False, description = "Test")

sp.user_playlist_create(user, name)

username = '*my username*' 
token = util.prompt_for_user_token(
    username=username,
    scope='playlist-modify-public', 
    client_id=cid, 
    client_secret=secret, 
    redirect_uri="http://localhost:8888/callback"
)
sp = spotipy.Spotify(auth=token)


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


token = getAccessToken(cid, secret)

scope = 'playlist-modify-private'

r = requests.post('https://api.spotify.com/v1/users/brandon596/playlists',
                  headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token},
                  data = {"Name": "Test",
                          "Description": "Test",
                          "public": False})


#Requesting Authorization
r = requests.get('https://accounts.spotify.com/authorize', params = {
                 'client_id': cid,
                 'response_type': 'code',
                 'redirect_uri': redirect_uri,
                 'scope': scope,
                 'state': 'state'})

#Requesting Access Token
r2 = requests.post('https://accounts.spotify.com/api/token',
                   headers = {'Content-Type': 'application/x-www-form-urlencoded'},
                   data = {'grant_type': 'authorization_code',
                           'code': code,
                           'redirect_uri': redirect_uri})




