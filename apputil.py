import os
import requests
from dotenv import load_dotenv

class Genius:


    def __init__(self, access_token=None):
        load_dotenv()
        self.access_token = access_token

        self.base_url = "https://api.genius.com"
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    def search(self, search_term):
        url = f"{self.base_url}/search"
        response = requests.get(url, params={"q": search_term}, headers=self.headers)
        return response.json()
    
    def get_artist_id(self, search_data):
        hits = search_data.get("response", {}).get('hits', [])
        if not hits:
            print("No hits found")
            return None
        artist_id = hits[0].get('result', {}).get('primary_artist', {}).get('id')
        return artist_id

    def get_artist(self, search_term):
        search_data = self.search(search_term)
        artist_id = self.get_artist_id(search_data)

        artist_link = f"{self.base_url}/artists/{artist_id}"
        artist_response = requests.get(artist_link, headers=self.headers)

        return artist_response
    
    def get_artists(self, search_terms):
        results = []
        
        return 0