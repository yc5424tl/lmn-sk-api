import json
import os
from logging import Logger

import sk_factory as Factory
from api_models.sk_artist import Artist
from api_models.sk_event import Event
from api_models.sk_venue import Venue
from sk_query_mgr import Query

search_ip_endpoint = "http://api.songkick.com/api/3.0/events.json?apikey={}&location=ip:{}"
log = Logger
Query = Query()



class API:

    def __init__(self):
        self.key = os.getenv('SK_API_KEY')


    @staticmethod
    def search_for_artist(artist_name: str, match_first: bool) -> Artist or False:
        response_dict = Query.search_artists_by_name(artist_name, match_first=match_first)
        try:
            if match_first:
                # return Factory.instance_call(response_dict, class_call=Artist)
                new_artist = Factory.build_artist(response_dict)
                return new_artist
            else:
                matching_artists_list = []
                for artist in response_dict:
                    # matching_artists_list.append(Factory.instance_call(artist, class_call=Artist))
                    new_artist = Factory.build_artist(artist)
                    matching_artists_list.append(new_artist)
                return matching_artists_list
        except TypeError:
            return False


    def search_venues(self, venue_name: str) -> [Venue]:
        venue_dict_list = Query.search_venues_by_name(venue_name)
        if len(venue_dict_list) == 0:
            return []
        else:
            venue_list = self.instantiate_list_data(venue_dict_list, call=Venue)
            return venue_list


    def search_artist_id_for_upcoming_events(self, artist_id: int) -> [Event]:
        event_dict_list = Query.search_artist_upcoming_events(artist_id)
        if len(event_dict_list) == 0:
            return []
        else:
            events_list = self.instantiate_list_data(event_dict_list, call=Event)
            return events_list


    def search_venue_id_for_upcoming_events(self, venue_id: int) -> [Event]:
        event_dict_list = Query.search_venue_upcoming_events(venue_id)
        if len(event_dict_list) == 0:
            return []
        else:
            events_list = self.instantiate_list_data(event_dict_list, call=Event)
            return events_list


    def search_events_near_ip(self, ip_addr: str) -> [{}]:
        if ip_addr == '127.0.0.1':
            ip_addr = '67.220.22.82'
        event_dict_list = Query.search_events_by_ip_location(ip_addr)
        if len(event_dict_list) == 0:
            return []
        else:
            events_list = self.instantiate_list_data(event_dict_list, call=Event)
            return events_list


    @staticmethod
    def instantiate_events_from_list(event_list: [{}]) -> [Event]:
        if len(event_list) == 0:
            return []
        else:
            events = []
            for event in event_list:
                try:
                    new_event = Factory.build_event(event)
                    events.append(new_event)
                except KeyError as kE:
                    log(f'Key not present in event(dict): {str(kE)}')
            return events


    @staticmethod
    def instantiate_venues_from_list(venue_list: [{}]) -> [Venue]:
        if len(venue_list) == 0:
            return []
        else:
            venues_list = []
            for venue in venue_list:
                new_venue = Factory.build_venue(venue)
                venues_list.append(new_venue)
            return venues_list

    @staticmethod
    def instantiate_artists_from_list(artist_list: [{}]) -> [Artist]:
        if not bool(len(artist_list)):
            return []
        else:
            artists_list = []
            for artist in artist_list:
                new_artist = Factory.build_artist(artist)
                artists_list.append(new_artist)
            return artists_list

    @staticmethod
    def instantiate_list_data(list_data:[{}], call):
        if not bool(len(list_data)):
            return []
        else:
            instance_list = []
            for data in list_data:
                try:
                    new_instance = Factory.instance_call(list_data=data, class_call=call)
                    instance_list.append(new_instance)
                except KeyError as kE:
                    log(f'KeyError {kE} during {call} instance call passing {data}')
            return instance_list

    @staticmethod
    def serialize_list(dict_list: [{}]):
        serial_list = []
        for obj in dict_list:
            serial_list.append(json.dumps(obj, default=lambda o: getattr(o, '__dict__', str(o))))
        return serial_list


# @staticmethod
# def get_external_ip():
#     ip_address = requests.get('https://api.ipify.org?format=json').json()
#     ip = ip_address['ip']
#     return ip
# def proof_search_artist(test_artist_name):
#     artists = search_for_artist(test_artist_name)
#     count = 1
#     selection_list = []
#     for artist in artists:
#         selection_list.append({'name': artist.displayName, 'id': artist.sk_id})
#         print(str(count) + ': ' + artist.displayName)
#         count += 1
#     selection = ''
#     while not selection:
#         selection = input('Enter # to select Artist')
#     selected_artist = selection_list[int(selection) - 1]['name']
#     for artist in artists:
#         if artist.displayName == selected_artist:
#             print(artist.__str__())
#
#
# def proof_foo_event_search(events: [Event]):
#     for event in events:
#         print('=================================\n'
#               '=================================\n'
#               '=================================\n')
#         print(event.__str__())