import concurrent.futures
# from multiprocessing import Pool, cpu_count
import multiprocessing

from api_models.sk_metro_area import MetroArea
from sk_query_mgr import Query
from api_models.sk_artist import Artist
from api_models.sk_city import City
from api_models.sk_event import Event
from api_models.sk_location import Location
from api_models.sk_performance import Performance
from api_models.sk_venue import Venue
Query = Query()
from logging import Logger

log = Logger

event_count = 0
venue_count = 0
location_count = 0
artist_count = 0
performance_count = 0



def instance_call(list_data: [{}], call: str):
    if not list_data:
        return []
    else:
        factory = Factory()
        switcher = {
            'artist': factory.build_artist,
            'city': factory.build_city,
            'event': factory.build_event,
            'location': factory.build_location,
            'venue': factory.build_venue,
            'metro_area': factory.build_metro_area,
            'performance': factory.build_performances
        }
        function_call = switcher.get(call)
        return function_call(list_data)



class Factory(object):
    def __init__(self):
        self.event_count = 0
        self.venue_count = 0
        self.location_count = 0
        self.artist_count = 0
        self.performance_count = 0
        self.city_count = 0
        self.metro_count = 0

    def build_artist(self, artist_data: dict) -> Artist or None:
        try:
            self.artist_count += 1
            return Artist(
                sk_id         = artist_data['id'],
                display_name  = artist_data['displayName'],
                uri           = artist_data['uri'],
                tour_end_date = artist_data['onTourUntil'] )
        except Exception as exc:
            print(f'Exception in factory.build_artist -> {exc}')
            return None

    def build_artist_by_name(self, artist_name: str) -> Artist:
        artist_dict = Query.search_artists_by_name(artist_name, match_first=True)
        new_artist = self.build_artist(artist_dict)
        return new_artist



    def build_city(self, city_data: dict) -> City:
        self.city_count += 1
        return City(
            sk_id   = city_data['id'],
            name    = city_data['displayName'],
            uri     = city_data['uri'],
            country = city_data['country'])


    def build_event(self, ed: dict) -> Event or None:
        #print('sk_factory.build_event')
        # print('build_event')
        # print(f'event_count: {self.event_count}')
        self.event_count += 1

        # key_list = ['id', 'displayName', 'type', 'uri', 'status', 'popularity', 'start', 'performance', 'ageRestriction', 'flaggedAsEnded', 'venue', 'location', 'end', 'series']

        # for k in ed.keys():
        #     if not key_list.__contains__(k):
        #         print(f'Key not in Key List, key from -> {ed.keys()}')
        #         return None
        # print('returning event object')
        # print(f"\n\ndisplayName: {ed['displayName']}\n"
        #       f"type:{ed['type']}\n"
        #       f"popularity: {ed['popularity']}\n"
        #       f"id:{ed['id']}\n"
        #       f"start:{ed['start']}\n"
        #       f"status:{ed['status']}\n"
        #       f"uri:{ed['uri']}\n\n")

        event = Event(ed)
        # event = Event(
        #     display_name=ed['displayName'],
        #     event_type=ed['type'],
        #     # location     = self.build_location(event_data['location']),
        #     # performances = self.build_performances(event_data['performance']),
        #     popularity=ed['popularity'],
        #     sk_id=ed['id'],
        #     start=ed['start'],
        #     status=ed['status'],
        #     uri=ed['uri'])
        #print(f'\n\nevent of type {type(event)} -> {event}')
        # try:
        #     log(f'Returning object type:{type(event)} of value:{event.__dict__()}')
        # except AttributeError as aE:
        #     print(f'{aE}, ed -> {ed}')
        # log(f'type(event.result()) = {type(event.result())}')
        return event



            # if ed['displayName'] and ed['type']  and \
            #         ed['id'] and ed['start'] and ed['status'] and ed['uri']:
            # if event_data['displayName'] and event_data['type'] and event_data['location'] and event_data['performance'] and event_data['popularity'] and event_data['id'] and event_data['start'] and event_data['status'] and event_data['uri']:
            #     return Event(
            #         display_name = ed['displayName'],
            #         event_type   = ed['type'],
            #         # location     = self.build_location(event_data['location']),
            #         # performances = self.build_performances(event_data['performance']),
            #         popularity   = ed['popularity'],
            #         sk_id        = ed['id'],
            #         start        = ed['start'],
            #         status       = ed['status'],
            #         uri          = ed['uri'])
                    # venue        = self.build_venue_by_id(int(event_data['venue']['id'])) if event_data['venue']['id'] else None)
            # else:
            #     print(f'incomplete event data -> \n\n{ed}\n\n')
            #     print(f"keys: {ed.keys()} id: {ed['id']} type: {ed['type']} pop: {ed['popularity']} start: {ed['start']} status: {ed['status']} uri: {ed['uri']} displayName: {ed['displayName']}")
        # except KeyError as kE:
        #     print(f'KeyError: {kE}')
        #     return None
        # except Exception as exc:
        #     print(f'Exception: {exc} from event_data -> {ed}')
        #     return None

    @staticmethod
    def concurrent_build_events(event_data:[{}]):
        from api_models.sk_event import Event
        if __name__ == 'sk_factory':
            p = multiprocessing.Pool()
            sk_events = p.map(Event, [sk_event for sk_event in event_data])
            p.close()
            p.join()
            return sk_events

        # print('in top of concurrent_build_events')
        # # print(f'__name__ == {__name__}')
        # print(f'KEYS: {event_data[0].keys()}')
        # event_list = None
        # if __name__ == 'sk_factory':
        #     try:
        #         pool = multiprocessing.Pool.
        #         print('building event list')
        #         event_list = Pool(5).map(self.build_event, event_data[0:10])
        #         # print(f'event_data[0:5] -> {event_data[0:5]}')
        #         print(f'type of event list -> {type(event_list)}')
        #         print(f'type event_list[0] -> {type(event_list[0])}')
        #         print(f'\n\nreturning event list -> {event_list}\n\n')
        #         return event_list
        #     except Exception as tE:
        #         print(f'Exception in factory.concurrent_build_events -> {tE}')
        #         return event_list
        # else:
        #     print('__name__ != sk_factory')

        # with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        #     future_to_event = [executor.submit(self.build_event, )]
            # instantiated_events_list = [event.result() for event in executor.map(self.build_event, event_data)]
            # return instantiated_events_list


            # future_to_event = [executor.submit(self.build_event, event) for event in event_data]
            # for future in concurrent.futures.as_completed(future_to_event):
            #     try:
            #         data = future.result()
            #         print(f'type(data) -> {type(data)}')
            #         event_list.append(data)
            #     except Exception as exc:
            #         print(f'exception {exc}')
            #     else:
            #         pass
            # print(f'len(event_list) -> {len(event_list)}')
            # return event_list


    def build_location(self, location_data: dict) -> Location or None:
        self.location_count += 1
        try:
            return Location(
                city = location_data['city'],
                lat  = location_data['lat'],
                lng  = location_data['lng'])
        except Exception as exc:
            print(f'Exception {exc} in build_location, {exc}) ')
            return None



    def build_metro_area(self, metro_area_data: dict) -> MetroArea or None:
        try:
            self.metro_count += 1
            return MetroArea(
                sk_id        = metro_area_data['id'],
                uri          = metro_area_data['uri'],
                display_name = metro_area_data['displayName'],
                country      = metro_area_data['country'])
        except Exception as exc:
            print(f'Exception in factory.build_metro_area -> {exc}')
            return None

    def build_performances(self, performance_data: [{}]) -> [Performance]:
        performance_list = []
        for performance in performance_data:
            try:
                self.performance_count += 1
                new_performance =  Performance(
                        artist        = self.build_artist_by_name(performance['artist']['displayName']),
                        billing       = performance['billing'],
                        billing_index = performance['billingIndex'],
                        name          = performance['displayName'],
                        sk_id         = performance['id'])
                performance_list.append(new_performance)
            except Exception as exc:
                print(f'Exception in factory.build_performances -> {exc}')
        return performance_list


    def build_venue(self, venue_data: dict) -> Venue or None:
        try:
            self.venue_count += 1
            # import pprint
            # pp = pprint.PrettyPrinter()
            # pp.pprint(venue_data)
            # print(f'type(venue_data) = {type(venue_data)}')
            if venue_data['capacity'] is None:
                venue_capacity = -1
            else:
                venue_capacity = venue_data['capacity']
            return Venue(
                capacity    = venue_capacity,
                city        = venue_data['city'],
                description = venue_data['description'],
                lat         = venue_data['lat'],
                lng         = venue_data['lng'],
                metro_area  = self.build_metro_area(venue_data['metroArea']),
                name        = venue_data['displayName'],
                phone       = venue_data['phone'],
                sk_id       = venue_data['id'],
                street      = venue_data['street'],
                uri         = venue_data['uri'],
                website     = venue_data['website'],
                zip_code    = venue_data['zip'])
        except Exception as exc:
            print(f'Exception in factory.build_venue -> {exc}')
            return None


    def build_venue_by_id(self, venue_id: int) -> Venue or None:
        try:
            venue_data = Query.search_venue_by_id(venue_id)
            return self.build_venue(venue_data)
        except Exception as exc:
            print(f'Exception in factory.build_venue_by_id -> {exc}')
            return None

    def total_objects(self):
        return self.artist_count + self.performance_count + self.location_count + self.event_count + self.venue_count + self.metro_count







