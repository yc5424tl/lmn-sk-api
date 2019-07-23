
import os
import requests

api_key = os.getenv('SK_API_KEY')

def execute(endpoint: str, query: str or int, match_first=None) -> dict:

    switcher = {
        'artist_name': {
            'url': f"https://api.songkick.com/api/3.0/search/artists.json?apikey={api_key}&query={query}",
            'target': 'artist'},

        'artist_upcoming': {
            'url': f"https://api.songkick.com/api/3.0/artists/{query}/calendar.json?apikey={api_key}",
            'target': 'event'},

        'local_events': {
            'url': f"https://api.songkick.com/api/3.0/events.json?apikey={api_key}&location=ip:{query}",
            'target': 'event'},

        'venue_id': {
            'url': f"https://api.songkick.com/api/3.0/venues/{query}.json?apikey={api_key}",
            'target': 'venue'},

        'venue_name': {
            'url': f"https://api.songkick.com/api/3.0/search/venues.json?query={query}&apikey={api_key}",
            'target': 'venue'},

        'venue_upcoming': {
            'url': f"https://api.songkick.com/api/3.0/venues/{query}/calendar.json?apikey={api_key}",
            'target': 'event'}
        }

    response = requests.get(switcher[endpoint]['url']).json()
    target = switcher[endpoint]['target']

    try:
        if match_first:
            target_data = response['resultsPage']['results'][target][0]
        else:
            target_data = response['resultsPage']['results'][target]
        return target_data

    except KeyError as kE:
        print(f'{kE}')
        if response['resultsPage']['status'] == 'error':
            return response['resultsPage']['error']



# class Query(object):
#     def __init__(self):
#         self.artist_events_url = "https://api.songkick.com/api/3.0/artists/{}/calendar.json?apikey={}"
#         self.artists_url       = "https://api.songkick.com/api/3.0/search/artists.json?apikey={}&query={}"
#         self.ip_events_url     = "https://api.songkick.com/api/3.0/events.json?apikey={}&location=ip:{}"
#         self.key               = os.getenv('SK_API_KEY')
#         self.venue_events_url  = "https://api.songkick.com/api/3.0/venues/{}/calendar.json?apikey={}"
#         self.venue_id_url      = "https://api.songkick.com/api/3.0/venues/{}.json?apikey={}"
#         self.venues_url        = "https://api.songkick.com/api/3.0/search/venues.json?query={}&apikey={}"
#
#
#     @staticmethod
#     def get_city_by_venue(venue_dict: dict) -> dict:
#         city_data = venue_dict['city']
#         return city_data
#
#
#     def search_artists_by_name(self, artist_name: str, match_first: bool) -> dict:
#         response = requests.get(self.artists_url.format(self.key, artist_name)).json()
#         try:
#             if match_first:
#                 artists_data = response['resultsPage']['results']['artist'][0]
#             else:
#                 artists_data = response['resultsPage']['results']['artist']
#             return artists_data
#         except KeyError:
#             if response['resultsPage']['status'] == 'error':
#                 return response['resultsPage']['error']
#
#
#     def search_artist_upcoming_events(self, artist_id: int) -> list:
#         response = requests.get(self.artist_events_url.format(artist_id, self.key)).json()
#         try:
#             event_data = response['resultsPage']['results']['event']
#             return event_data
#         except KeyError:
#             if response['resultsPage']['status'] == 'error':
#                 return response['resultsPage']['error']
#
#
#     def search_events_by_ip_location(self, ip_addr) -> list:
#         response = requests.get(self.ip_events_url.format(self.key, ip_addr)).json()
#         try:
#             event_data = response['resultsPage']['results']['event']
#             return event_data
#         except KeyError:
#             if response['resultsPage']['status'] == 'error':
#                 return response['resultsPage']['error']
#
#
#     def search_venue_by_id(self, venue_id: int):
#         response = requests.get(self.venue_id_url.format(venue_id, self.key)).json()
#         try:
#             venue_data = response['resultsPage']['results']['venue']
#             return venue_data
#         except KeyError:
#             if response['resultsPage']['status'] == 'error':
#                 return response['resultsPage']['error']
#
#
#     def search_venues_by_name(self, venue_name: str, match_first: bool) -> list:
#         response = requests.get(self.venues_url.format(venue_name, self.key)).json()
#         try:
#             if match_first:
#                 venue_data = response['resultsPage']['results']['venue'][0]
#             else:
#                 venue_data = response['resultsPage']['results']['venue']
#             return venue_data
#         except KeyError:
#             if response['resultsPage']['status'] == 'error':
#                 return response['resultsPage']['error']
#
#
#     def search_venue_upcoming_events(self, venue_id: int) -> list:
#         response = requests.get(self.venue_events_url.format(venue_id, self.key)).json()
#         try:
#             event_data = response['resultsPage']['results']['event']
#             return event_data
#         except KeyError:
#             if response['resultsPage']['status'] == 'error':
#                 return response['resultsPage']['error']