import concurrent
import datetime
import os
import pprint
from concurrent.futures import as_completed

import requests

pp = pprint.PrettyPrinter()



class Query(object):
    def __init__(self):
        self.artist_events_url     = "https://api.songkick.com/api/3.0/artists/{}/calendar.json?apikey={}"
        self.artists_url           = "https://api.songkick.com/api/3.0/search/artists.json?apikey={}&query={}"
        self.gigography_url        = "https://api.songkick.com/api/3.0/artists/{}/gigography.json?apikey={}"
        self.ip_events_url         = "https://api.songkick.com/api/3.0/events.json?apikey={}&location=ip:{}"
        self.key                   = os.getenv('SK_API_KEY')
        self.metro_area_events_url = "https://api.songkick.com/api/3.0/metro_areas/{}/calendar.json?apikey={}"
        self.venue_events_url      = "https://api.songkick.com/api/3.0/venues/{}/calendar.json?apikey={}"
        self.venue_id_url          = "https://api.songkick.com/api/3.0/venues/{}.json?apikey={}"
        self.venues_url            = "https://api.songkick.com/api/3.0/search/venues.json?query={}&apikey={}"
        self.event_count = 0



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



    # @executor.job
    def conc_get_events_by_ip_page(self, ip_addr, page_num):
        # print('TOP OF CONC_GET_EVENTS_BY_IP_PAGE')
        if ip_addr == '127.0.0.1':
            ip = '67.220.22.82'
        else:
            ip = ip_addr
        response_page = requests.get(self.ip_events_url.format(self.key, ip), params={'page': page_num}).json()
        page_events = []

        try:
            for event in response_page['resultsPage']['results']['event']:
                page_events.append(event)
        except KeyError as kE:
            if 'clientLocation' in response_page["resultsPage"].keys():
                print('clientLocation in response_page')
            else:
                print(f'Key Error: {kE} processing page {page_num}')
                print(f'type(page_events): {type(page_events)} len(page_events): {len(page_events)}')
        return page_events


    def conc_search_events_by_ip_location(self, ip_addr):
        # print('TOP OF CONC_SEARCH_EVENTS_BY_I_LOC')
        if ip_addr == '127.0.0.1':
            ip = '67.220.22.82'
        else:
            ip = ip_addr
        response = requests.get(self.ip_events_url.format(self.key, ip)).json()
        print(f'type(response_page) -> {type(response)}')
        print(response['resultsPage']['results'].keys())
        event_dict_list = response['resultsPage']['results']['event']
        object_count = response['resultsPage']['totalEntries']
        num_pages = round(object_count/50) -1

        # num_pages = response['resultsPage']['totalEntries']
        event_dicts = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
            future_to_event = [executor.submit(self.conc_get_events_by_ip_page, ip_addr, i) for i in range(2, num_pages+1)]
            for future in concurrent.futures.as_completed(future_to_event):
                try:
                    data = future.result()
                    # print(f'type(data) -> {type(data)}')
                    for event in data:
                        # print(f'type(event) in data -> {type(event)}')
                        event_dicts.append(event)
                        # print(f'len(event_dicts) -> {len(event_dicts)}')
                except Exception as exc:
                    print(f'exception {exc}')
                else:
                    pass
            event_dict_list.extend(event_dicts)
            return event_dict_list



    def search_events_by_ip_location(self, ip_addr) -> list:
        start_time = datetime.datetime.now()
        response = requests.get(self.ip_events_url.format(self.key, ip_addr)).json()
        event_dict_list = response['resultsPage']['results']['event']
        num_pages = response['resultsPage']['totalEntries']
        for page in range(2, num_pages + 1):
            next_page_response = requests.get(self.ip_events_url.format(self.key, ip_addr), params={'page': page}).json()
            try:
                for event in next_page_response['resultsPage']['results']['event']:
                    event_dict_list.append(event)
                    self.event_count += 1
            except KeyError:
                print("keyerror search vy ip")
                end_time = datetime.datetime.now()
                time_delta = end_time - start_time
                print(f'time_delta = {time_delta}')
                return event_dict_list
                #if 'clientLocation' in next_page_response["resultsPage"].keys():


        print(f'total number of events: {self.event_count}')
        end_time = datetime.datetime.now()
        time_delta = end_time - start_time
        print(f'time_delta = {time_delta}')
        return event_dict_list


    def search_events_by_metro_area(self, metro_area_id: int):
        response_data = requests.get(self.metro_area_events_url.format(metro_area_id, self.key)).json()
        event_dict_list = response_data['resultsPage']['results']['event']
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



