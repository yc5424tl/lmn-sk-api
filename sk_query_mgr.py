
import os
import requests
import pprint

pp = pprint.PrettyPrinter()

class Query(object):
    def __init__(self):
        self.artist_events_url = "https://api.songkick.com/api/3.0/artists/{}/calendar.json?apikey={}"
        self.artists_url       = "https://api.songkick.com/api/3.0/search/artists.json?apikey={}&query={}"
        self.gigography_url    = "https://api.songkick.com/api/3.0/artists/{}/gigography.json?apikey={}"
        self.ip_events_url     = "https://api.songkick.com/api/3.0/events.json?apikey={}&location=ip:{}"
        self.key               = os.getenv('SK_API_KEY')
        self.metro_area_events_url = "https://api.songkick.com/api/3.0/metro_areas/{}/calendar.json?apikey={}"
        self.venue_events_url  = "https://api.songkick.com/api/3.0/venues/{}/calendar.json?apikey={}"
        self.venue_id_url      = "https://api.songkick.com/api/3.0/venues/{}.json?apikey={}"
        self.venues_url        = "https://api.songkick.com/api/3.0/search/venues.json?query={}&apikey={}"


    @staticmethod
    def get_city_by_venue(venue_dict: dict) -> dict:
        city_data = venue_dict['city']
        return city_data

    def gigography(self, artist_id: int):
        response = requests.get(self.gigography_url.format(artist_id, self.key)).json()
        event_dict_list =  response['resultsPage']['results']['event']
        num_pages = response['resultsPage']['totalEntries']
        for page in range(2, num_pages+1):
            next_page_response = requests.get(self.gigography_url.format(artist_id, self.key), params={'page': page}).json()
            try:
                new_event_dict_list = next_page_response['resultsPage']['results']['event']
                event_dict_list.append(new_event_dict_list)
            except KeyError:
                if 'clientLocation' in next_page_response['resultsPage'].keys():
                    break


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
        num_pages = response['resultsPage']['totalEntries']
        for page in range(2, num_pages +1):
            next_page_response = requests.get(self.ip_events_url.format(self.key, ip_addr), params={'page': page}).json()
            try:
                new_events_dict_list = next_page_response['resultsPage']['results']['event']
                event_dict_list.append(new_events_dict_list)
            except KeyError:
                if 'clientLocation' in next_page_response["resultsPage"].keys():
                    break
        return event_dict_list


    def search_events_by_metro_area(self, metro_area_id: int):
        response = requests.get(self.metro_area_events_url.format(metro_area_id, self.key))
        event_dict_list = response['resultsPage']['results']['event']
        return event_dict_list

    def search_venue_by_id(self, venue_id: int):
        response = requests.get(self.venue_id_url.format(venue_id, self.key)).json()
        venue_dict = {}
        if response['resultsPage']['results']:
            venue_dict = response['resultsPage']['results']['venue']
        return venue_dict


    def search_venues_by_name(self, venue_name: str, first_match: bool) -> list:
        response = requests.get(self.venues_url.format(venue_name, self.key)).json()
        venue_dict_list = []
        if response['resultsPage']['results']:
            if first_match:
                venue_dict_list = [response['resultsPage']['results']['venue'][0]] # list containing dicts of venue data
            if not first_match:
                venue_dict_list = response['resultsPage']['results']['venue']
        return venue_dict_list


    def search_venue_upcoming_events(self, venue_id: int) -> list:
        response = requests.get(self.venue_events_url.format(venue_id, self.key)).json()
        event_dict_list = []
        if response['resultsPage']['results']:
            event_dict_list = response['resultsPage']['results']['event']
        return event_dict_list



