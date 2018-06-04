# -*- coding: utf-8 -*-
"""
Scrape genius.com for song lyrics and write out.
"""

import requests
import urllib2
import json
from bs4 import BeautifulSoup
import re
import pprint

# Keys 
client_ID = 'iS3GYpBAJT4HiVwXbcqGVve9esOSqiCUkYGzOVBzHWbW3o2c7ChjMkEgMtpAsAM5'
client_secret = 'Qr1O5qanrhv-rocPKGClOzb1I8HmvJJVcHdAbShhXJrIvLTHg-dTfeJ5jlvtMxNCaka1OP9myVcjxNidCkTxyg'
client_access_token = 'A9E6664U_jZVDQmRvZTjgbbXinigqzztzaaIc8_xFuateNaOngJhwTeQuJQRYx5F'




# Search terms
search_term = "mount eerie"




# General search
_URL_API = "https://api.genius.com/"
_URL_SEARCH = "search?q="
querystring = _URL_API + _URL_SEARCH + urllib2.quote(search_term)
# Format a request URL for the Genius API
request = urllib2.Request(querystring)
request.add_header("Authorization", "Bearer " + client_access_token)
request.add_header("User-Agent", "") 
# requests query
response = urllib2.urlopen(request, timeout=3)
raw = response.read()
json_obj = json.loads(raw)   #if song - ['response']['song']



# Search for artists ID
artist_id = json_obj['response']['hits'][0]['result']['primary_artist']['id']



# Find songs associated with artists ID
for page_count in range(1, 3):
    querystring = "https://api.genius.com/artists/" + str(artist_id) + \
                                   '/songs?per_page=50&sort=popularity' + \
                                   '&page=' + str(page_count)
    # Format a request URL for the Genius API
    request = urllib2.Request(querystring)
    request.add_header("Authorization", "Bearer " + client_access_token)
    request.add_header("User-Agent", "") 
    # requests query
    response = urllib2.urlopen(request, timeout=3)
    raw = response.read()
    json_obj = json.loads(raw)['response']['songs']
    song_list = [key['title'].replace(' ', '-') for key in json_obj]
    
    # Scrape lyrics
    artist = search_term.replace(' ', '-')
    end = '-lyrics'
    lyric_dict = {}
    for song in song_list:
        song = song
        URL = 'https://genius.com/' + artist + '-' + song + end
        page = requests.get(URL)    
        html = BeautifulSoup(page.text, "html.parser") # Extract the page's HTML as a string
    
        # Scrape the song lyrics from the HTML
        try:
            lyrics = html.find("div", class_="lyrics").get_text().encode('ascii','ignore')
            lyric_dict[song] = [lyrics]
        except AttributeError:
            continue
    
pprint.pprint(lyric_dict)