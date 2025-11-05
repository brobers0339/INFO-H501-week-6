#Third-party Imports
import requests
import pandas as pd
from dotenv import load_dotenv


class Genius:
    '''
    A client for interaction with the Client API.

    This class provides functions to search for songs or artists, retrieve
    artist information, and collection related information from the Genius API.

    Parameters
    ----------
    access_token : str, optional
        A valid Genius API access token for authentication.

    Attributes
    ----------
    base_url : str
        The base url for the Genius API
    headers : dict
        The HTTP headers for API requests, including the Authorization token.
    '''
    def __init__(self, access_token=None):
        '''
        Initialize the Genius client.

        This constructor sets up an authentication and configuration for communicating
        with the Genius API.

        Parameters
        ----------
        access_token : str, optional
            A valid Genius API access token used for authentication. 

        Attributes
        ----------
        base_url : str
            The base url for the Genius API
        headers : dict
            The HTTP headers for API requests, including the Authorization token.
        '''

        load_dotenv()
        self.access_token = access_token

        self.base_url = "https://api.genius.com"
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    def search(self, search_term):
        '''
        Use the Genius API url to search for the given artist name.

        This function uses the base Genius url and the given search term to 
        find the response JSON for the given artist to be utilized for further
        exploration.

        Paramters
        ---------
        search_term : str
            A string with the given artist name to be searched.

        Returns
        -------
        dict
            Returns a JSON response dictionary that is within the given search url.
        '''
        url = f"{self.base_url}/search"
        response = requests.get(url, params={"q": search_term}, headers=self.headers)
        return response.json()
    
    def get_artist_id(self, search_data):
        '''
        Retrieve the artist ID for the specific artist from the Genius API.

        The function uses the found response.json from the search method to 
        find the most likely artist ID based on the top hit from the Genius API.

        Parameters
        ----------
        search_data : dict
            The JSON response returned by the Genius API search method.

        Returns
        -------
        int or None
            The Genius artist ID of the first (aka top) search result.
            Returns None if no result is found.
        '''

        hits = search_data.get("response", {}).get('hits', [])
        artist_id = hits[0].get('result', {}).get('primary_artist', {}).get('id')
        return artist_id

    def get_artist(self, search_term):
        '''
        Retrieve artist information from the Genius API.

        This function performs a search for the given artist, uses previously defined
        function to extract the most likely artist ID, and retrieves the artist information
        from the Genius API.

        Parameters
        -----------
        search_term: str
            A string containing the artist name to look up on the Genius API.

        Returns
        -------
        dict
            Returns the JSON response from the Genius API including all known
            information on the given artist at that artist ID.
        '''

        search_data = self.search(search_term)
        artist_id = self.get_artist_id(search_data)

        artist_link = f"{self.base_url}/artists/{artist_id}"
        artist_response = requests.get(artist_link, headers=self.headers)

        return artist_response.json()
    
    def get_artists(self, search_terms):
        '''
        Retrieve multiple artist information from the Genius API.

        The function iterates over a list of artists that will be used as search terms,
        performs a search for each artist, extracts the most likely artist ID, 
        retrieves the artist information from the Genius API, and compiles the results
        into a pandas DataFrame.

        Parameters:
        -----------
        search_terms : list of str
            A list of artist names to look up on the Genius API and retrieve
            information for

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing one row per search term with the following information:
                - 'search_term' : the original artist name or search term provided
                - 'artist_name' : the artist name returned by the API
                - 'artist_id'   : the Genius artist ID
                - 'followers_count' : the number of followers for that artist 
        '''

        results = []


        for artist in search_terms:

            artist_info = self.get_artist(artist)

            artist_data = artist_info.get("response", {}).get("artist", {})
            
            artist_name = artist_data.get('name')
            num_followers = artist_data.get('followers_count')
            artist_id = artist_data.get('id')

            results.append({
                'search_term' : artist,
                'artist_name' : artist_name,
                'artist_id' : artist_id,
                'followers_count' : num_followers
            })

        return pd.DataFrame(results)