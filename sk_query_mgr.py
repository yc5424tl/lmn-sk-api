import concurrent
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
        print(f'IP: {ip_addr}  Page: {page_num}')
        response_page = requests.get(self.ip_events_url.format(self.key, ip_addr), params={'page': page_num}).json()
        # print(f'Response: {response_page}')
        print(f'Response Length for Page {page_num}: {len(response_page)}')
        page_events = []
        try:
            for event in response_page['resultsPage']['results']['event']:
                self.event_count += 1
                # print(f'Event Count: {self.event_count}')
                page_events.append(event)
        except KeyError as kE:
            if 'clientLocation' in response_page["resultsPage"].keys():
                pass
            print(f'Key Error: {kE} processing page {page_num}')
            pass
        return page_events


    def conc_search_events_by_ip_location(self, ip_addr):
        response = requests.get(self.ip_events_url.format(self.key, ip_addr)).json()
        event_dict_list = response['resultsPage']['results']['event']
        print(f'1) len(event_dict_list) = {len(event_dict_list)}')
        object_count = response['resultsPage']['totalEntries']
        # num_pages = round(object_count/50) -1
        num_pages = response['resultsPage']['totalEntries']
        print(f'Number of Pages: {num_pages}')
        # event_dict_list = self.conc_get_events_by_ip_page.map(ip_addr, range(2, num_pages + 1), event_dict_list)
        futures = []
        events = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
            future_to_event = [executor.submit(self.conc_get_events_by_ip_page, ip_addr, i) for i in range(2, num_pages+1)]
            print(f'type(future_to_event): {type(future_to_event)}')
            # print(f'future_to_event: {future_to_event}')
            print(f'future_to_event length -> {len(future_to_event)}')
            if future_to_event:
                print(f'future_to_event[0] -> {future_to_event[0]}')
            for future in concurrent.futures.as_completed(future_to_event):

                try:
                    data = future.result()
                    # print(f'data = {data}')
                    futures.append(data)
                    # print(f'type(data) -> {type(data)}')
                    # print(f'type(data[0]) -> {type(data[0])}')
                    for event in data:
                        events.append(event)

                        # if data[-1] == event:
                            # print(f'\n\ndata[-1] ->\n')
                            # print(event)
                            # print('\nend data[-1]\n\n')


                except Exception as exc:
                    # print('%r generated an exception: %s' % (event, exc))
                    print(f'exception {exc}')
                else:
                    # print('%r event is %d bytes' % (data, len(data)))
                    # futures.append(data)
                    pass
            print(f'event_dict_list length = {len(event_dict_list)}')
            print(f'events length = {len(events)}')
            event_dict_list.extend(events)
            print(f'after extend, length -> {len(event_dict_list)}')
            # print(f'event_dict_list -> {event_dict_list}')
            return event_dict_list
        # for i in range(2, int(num_pages) + 1):
        #     print(f'Executor Processing Page {i} ')
        #     future = executor.submit(self.conc_get_events_by_ip_page, ip_addr, i)
        #     futures.append(future)
        # events = []
        # for future in as_completed(futures):
        #     event = future.result()
        #     events.append(event)
        # return event_dict_list.extend(events)
        # for future in as_completed(futures):
        #     event = future.result()
        #     events.append(event)
        # return event_dict_list.extend(events)
        # event_list = executor.map(self.conc_get_events_by_ip_page, range(2, num_pages + 1), {'ip_addr': ip_addr})
        # event_dict_list.append(event_list)
        # print(f'2) len(event_dict_list) = {len(event_dict_list)}')


    def search_events_by_ip_location(self, ip_addr) -> list:
        response = requests.get(self.ip_events_url.format(self.key, ip_addr)).json()
        event_dict_list = response['resultsPage']['results']['event']
        print(f'initial len(event_dict_list) = {len(event_dict_list)}')
        num_pages = response['resultsPage']['totalEntries']
        for page in range(2, num_pages + 1):
            next_page_response = requests.get(self.ip_events_url.format(self.key, ip_addr), params={'page': page}).json()
            try:
                for event in next_page_response['resultsPage']['results']['event']:
                    event_dict_list.append(event)
                # new_events_dict_list = next_page_response['resultsPage']['results']['event']
                # event_dict_list.append(new_events_dict_list)

            except KeyError:
                if 'clientLocation' in next_page_response["resultsPage"].keys():
                    break
        print('\n\n=================START EVENT_DICT_LIST.APPENDED===================\n\n')
        pp.pprint(event_dict_list)
        print('\n\n=================END EVENT_DICT_LIST.APPENDED===================\n\n')
        print(f'type(event_dict_list) = {type(event_dict_list)}')
        print(f'len(event_dict_list) = {len(event_dict_list)}')
        for x in event_dict_list:
            if isinstance(x, dict) is False:
                print(f'type(x)={type(x)}')
                print(x)
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



