
import os
import requests
import pprint

pp = pprint.PrettyPrinter()

class Query(object):
    def __init__(self):
        self.artist_events_url = "https://api.songkick.com/api/3.0/artists/{}/calendar.json?apikey={}"
        self.artists_url       = "https://api.songkick.com/api/3.0/search/artists.json?apikey={}&query={}"
        self.ip_events_url     = "https://api.songkick.com/api/3.0/events.json?apikey={}&location=ip:{}"
        self.key               = os.getenv('SK_API_KEY')
        self.venue_events_url  = "https://api.songkick.com/api/3.0/venues/{}/calendar.json?apikey={}"
        self.venue_id_url      = "https://api.songkick.com/api/3.0/venues/{}.json?apikey={}"
        self.venues_url        = "https://api.songkick.com/api/3.0/search/venues.json?query={}&apikey={}"


    @staticmethod
    def get_city_by_venue(venue_dict: dict) -> dict:
        city_data = venue_dict['city']
        return city_data


    def search_artists_by_name(self, artist_name: str, match_first: bool) -> dict:
        response = requests.get(self.artists_url.format(self.key, artist_name)).json()
        if match_first:
            return response['resultsPage']['results']['artist'][0]
        else:
            return response['resultsPage']['results']['artist']


    def search_artist_upcoming_events(self, artist_id: int) -> list:
        response = requests.get(self.artist_events_url.format(artist_id, self.key)).json()
        event_dict_list = response['resultsPage']['results']['event']
        return event_dict_list


    def search_events_by_ip_location(self, ip_addr) -> list:
        response = requests.get(self.ip_events_url.format(self.key, ip_addr)).json()
        event_dict_list = response['resultsPage']['results']['event']
        return event_dict_list


    def search_venue_by_id(self, venue_id: int):
        response = requests.get(self.venue_id_url.format(venue_id, self.key)).json()
        venue_dict = response['resultsPage']['results']['venue']
        return venue_dict


    def search_venues_by_name(self, venue_name: str) -> list:
        response = requests.get(self.venues_url.format(venue_name, self.key)).json()
        venue_dict_list = response['resultsPage']['results']['venue'] # list containing dicts of venue data
        return venue_dict_list


    def search_venue_upcoming_events(self, venue_id: int) -> list:
        response = requests.get(self.venue_events_url.format(venue_id, self.key)).json()
        event_dict_list = response['resultsPage']['results']['event']
        return event_dict_list
