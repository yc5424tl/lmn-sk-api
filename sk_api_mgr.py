import json
import os
from logging import Logger

from api_models.sk_artist import Artist
from api_models.sk_event import Event
from api_models.sk_venue import Venue
from sk_query_mgr import Query



import time
from sk_factory import Factory, instance_call
import pprint
pp = pprint.PrettyPrinter()

search_ip_endpoint = "http://api.songkick.com/api/3.0/events.json?apikey={}&location=ip:{}"
log = Logger
Query = Query()
event_count = 0
fctry = Factory()



class API:
    def __init__(self):
        self.key = os.getenv('SK_API_KEY')
        self.factory = fctry



    def search_for_artist(self, artist_name: str, match_first: bool) -> [Artist] or False:
        response_dict = Query.search_artists_by_name(artist_name, match_first=match_first)
        try:
            if match_first:
                new_artist = self.factory.build_artist(response_dict)
                return [new_artist]
            else:
                matching_artists_list = []
                for artist in response_dict:
                    new_artist = self.factory.build_artist(artist)
                    matching_artists_list.append(new_artist)
                return matching_artists_list
        except TypeError:
            return False


    def search_venues(self, venue_name: str, first_match: bool) -> [Venue]:
        response = Query.search_venues_by_name(venue_name, first_match=first_match)
        pp.pprint(response)
        try:
            if first_match:
                pp.pprint(response)
                venue_list = self.instantiate_venues_from_list(response)
                print(f'venue list -> type: {type(venue_list)} value: {venue_list}')
                return venue_list
            else:
                venue_list = self.instantiate_venues_from_list(response)
                return venue_list
        except TypeError as tE:
            print(f'type error in search venues: {tE}')
            return False



        # if len(venue_dict_list) == 0:
        #     return []
        # else:
        #     venue_list = self.instantiate_venues_from_list(venue_dict_list)
        #     return venue_list


    def search_artist_id_for_upcoming_events(self, artist_id: int) -> [Event] or []:
        event_dict_list = Query.search_artist_upcoming_events(artist_id)
        if len(event_dict_list) == 0:
            return []
        else:
            events_list = self.instantiate_events_from_list(event_dict_list)
            return events_list

    def search_events_by_metro_area(self, metro_area_id: int) -> [Event] or []:
        event_dict_list = Query.search_events_by_metro_area(metro_area_id)
        if not event_dict_list:
            return []
        else:
            event_list = self.instantiate_events_from_list(event_dict_list)
            return event_list

    def search_artist_gigography(self, artist_id: int):
        event_dict_list = Query.gigography(artist_id)
        if not event_dict_list:
            return []
        else:
            event_list = self.instantiate_events_from_list(event_dict_list)
            return event_list

    def search_venue_id(self, venue_id: int) -> [Venue] or []:
        venue_dict = Query.search_venue_by_id(venue_id)
        if not venue_dict:
            return []
        else:
            venue_list = self.instantiate_venues_from_list([venue_dict])
            return venue_list


    def search_venue_id_for_upcoming_events(self, venue_id: int) -> [Event]:
        event_dict_list = Query.search_venue_upcoming_events(venue_id)
        if not event_dict_list:
            return []
        else:
            events_list = self.instantiate_events_from_list(event_dict_list)
            return events_list


    def search_events_near_ip(self, ip_addr: str) -> [] or [Event]:
        # from api_models.sk_event import Event
        # import sk_factory
        from sk_query_mgr import Query
        query = Query()
        # Query = Query()
        if ip_addr == '127.0.0.1':
            ip_addr = '67.220.22.82'
        event_dict_list = query.conc_search_events_by_ip_location(ip_addr)
        # event_dict_list = Query.search_events_by_ip_location(ip_addr)
        if not event_dict_list:
            print('event_dict_list returned empty')
            return []
        else:
            # print('sending event_dict_list to instantiate_events_from_list')
            # events_list = self.instantiate_events_from_list(event_dict_list)
            print(f'type(event_dict_list) = {type(event_dict_list)} from sk_api_mgr ln 125')
            print(f'len(event_dict_list) = {len(event_dict_list)}')
            # events_list = factory.concurrent_build_events(event_data=event_dict_list)
            # print(f'\n\n EVENT DICT LIST\n{event_dict_list}\nEND EVENT DICT LIST\n\n')
            sanitized_event_data = [e for e in event_dict_list if all(x in e.keys() for x in ['displayName', 'popularity', 'id', 'status', 'start', 'type'])]
            print(f'len(sanitized_event_data) = {len(sanitized_event_data)}')
            events_list = self.factory.concurrent_build_events(sanitized_event_data)


            # events_list = self.factory.concurrent_build_events(event_dict_list)
            print(f'type(events_list) *after factory* -> {type(events_list)}')
            return events_list




    # def send_to_build_event(self, event_data) -> Event:
    #     print(f'type(event)={type(event_data)}')
    #     # events = []
    #     # for event in event_list:
    #     try:
    #         # new_event = Factory.build_event(event_data)
    #         self.count += 1
    #         print(f'Instantiated Events: {self.count} from PID ')
    #         # events.append(new_event)
    #         # print(f'Instantiated Events added to List = {count}')
    #         # return new_event
    #     except KeyError as kE:
    #         log(f'Key not present in event(dict): {kE}')
    #         print(f'Key not present in event(dict): {kE}')
    #         print(f'Source Data: {event_data}')




    def instantiate_events_from_list(self, event_list: [{}]) -> [Event] or []:
        start_time = time.time()
        print(f'start time: {start_time}')
        if not event_list:
            return []
        else:
            # with Pool(maxtasksperchild=1) as pool:
            #     event_list = pool.map(self.send_to_build_event, event_list, chunksize=1)
            #     duration = time.time() - start_time
            #     print(f'Duration: {duration} (seconds?)')
            #     print('returning instantiated events list')
            #     return event_list

            #
            # pool = Pool()
            # results = [pool.map(self.send_to_build_event, event_list)]
            # print(f'Duration: {time.time()-start_time}')
            # return results

            # events = {}
            # count = 0
            # pool = multiprocessing.Pool()
            # for x in pool.imap(self.build_events_to_list, event_list):
            #     events[count]=x
            #     count += 1
            #     print(f'Instantiated Events: {count}     Time Elapsed:{time.time()-start_time}')
            # return [events]




            # jobs = []
            # events = []
            # for p in range(5):
            #     recv_end, send_end = multiprocessing.Pipe(False)
            #     process = multiprocessing.Process(target=self.build_events_to_list, args=(event_list, send_end))
            #     jobs.append(process)
            #     events.append(recv_end)
            #     process.start()
            # for proc in jobs:
            #     proc.join()
            # events_list = [x.recv() for x in events]


            # events = []
            # print('beginning to instantiate events list')
            # with multiprocessing.Pool() as pool:
            #     events = pool.map(self.build_events_to_list, event_list)
            events = []
            count = 0
            for event in event_list:
                try:
                    new_event = self.factory.build_event(event)
                    events.append(new_event)
                    count+=1
                    print(f'Instantiated Events = {count}')
                except KeyError as kE:
                    log(f'Key not present in event(dict): {str(kE)}')
                    print(f'Key not present in event(dict): {kE}')
                    print(f'Source Event: {event}')
            duration = time.time() - start_time
            print(f'Duration: {duration} (seconds?)')
            print('returning instantiated events list')
            return events



    def instantiate_venues_from_list(self, venue_list: [{}]) -> [Venue]:
        if len(venue_list) == 0:
            return []
        else:
            venues_list = []
            for venue in venue_list:
                new_venue = self.factory.build_venue(venue)
                venues_list.append(new_venue)
            return venues_list


    def instantiate_artists_from_list(self, artist_list: [{}]) -> [Artist]:
        if not artist_list:
            return []
        else:
            artists_list = []
            for artist in artist_list:
                try:
                    new_artist = self.factory.build_artist(artist)
                    artists_list.append(new_artist)
                except KeyError as kE:
                    log(f'KeyError {kE} during instantiating artists from list passing {artist}')
            return artists_list

    @staticmethod
    def instantiate_list_data(list_data:[{}], call: str):
        if not bool(len(list_data)):
            return []
        else:
            instance_list = []
            for data in list_data:
                try:
                    new_instance = instance_call(list_data=data, call=call)
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