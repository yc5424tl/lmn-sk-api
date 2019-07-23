
import os
from logging import Logger

import sk_factory as Factory
import sk_query_mgr as Query

from api_models.sk_artist import Artist
from api_models.sk_event import Event
from api_models.sk_venue import Venue

import pprint
pp = pprint.PrettyPrinter()
log = Logger

class API:

    def __init__(self):
        self.key = os.getenv('SK_API_KEY')


    def search_artists(self, artist_name: str, match_first: bool) -> Artist or False:
        artist_data = Query.execute(endpoint='artist_name', query=artist_name, match_first=match_first)
        artist_list = self.instantiate_list_data(artist_data, call=Artist)
        return artist_list


    def search_venues(self, venue_name: str, match_first: bool) -> [Venue]:
        venue_data = Query.execute(endpoint='venue_name', query=venue_name, match_first=match_first)
        venue_list = self.instantiate_list_data(venue_data, call=Venue)
        return venue_list


    def search_artist_id_for_upcoming_events(self, artist_id: int) -> [Event]:
        event_data = Query.execute(endpoint='artist_upcoming', query=artist_id)
        events_list = self.instantiate_list_data(event_data, call=Event)
        return events_list


    def search_venue_id_for_upcoming_events(self, venue_id: int, match_first: bool) -> [Event]:
        event_data = Query.execute(endpoint='venue_upcoming', query=venue_id, match_first=match_first)
        # print('\n\n=========================START EVENT DATA==============================\n\n')
        # pp.pprint(event_data)
        # print('\n\n===========================END EVENT DATA==============================\n\n')
        # for event in event_data:
        #     print('\n\n++++++++++++++++++++++++START SINGLE EVENT+++++++++++++++++++++++++\n\n')
        #     pp.pprint(event)
        #     print('\n\n+++++++++++++++++++++++END SINGLE EVENT++++++++++++++++++++++++++++\n\n')
        events_list = self.instantiate_list_data(event_data, call=Event)
        return events_list


    def search_events_near_ip(self, ip_addr: str) -> [Event]:
        if ip_addr == '127.0.0.1':
            ip_addr = '67.220.22.82'
        event_data = Query.execute(endpoint='local_events', query=ip_addr)
        events_list = self.instantiate_list_data(event_data, call=Event)
        return events_list


    @staticmethod
    def instantiate_list_data(list_data:[{}], call):
        if not list_data:
            return []
        else:
            print('have list_data')
            pp.pprint(f'list_data -> {list_data}')
            instance_list = []
            for data in list_data:
                try:
                    pp.pprint(f'data in list_data -> {data}')
                    new_instance = Factory.instance_call(data, call)
                    pp.pprint(f'New Instance ->')
                    pp.pprint(new_instance)
                    instance_list.append(new_instance)
                except KeyError as kE:
                    print(kE)
                    log(f'KeyError {kE} during {call} instance call passing {data}')
                except TypeError as tE:
                    print(tE)
                    log(f'TypeError {tE} during {call} instance call passing {data}')
            return instance_list



