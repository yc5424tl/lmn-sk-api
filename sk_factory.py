from api_models.sk_metro_area import MetroArea
from sk_query_mgr import Query
from api_models.sk_artist import Artist
from api_models.sk_city import City
from api_models.sk_event import Event
from api_models.sk_location import Location
from api_models.sk_performance import Performance
from api_models.sk_venue import Venue

Query = Query()

event_count = 0
venue_count = 0
location_count = 0
artist_count = 0
performance_count = 0



def instance_call(list_data: [{}], call: str):
    if not bool(len(list_data)):
        return []
    else:
        switcher = {
            'artist': Factory.build_artist,
            'city': Factory.build_city,
            'event': Factory.build_event,
            'location': Factory.build_location,
            'venue': Factory.build_venue,
            'metro_area': Factory.build_metro_area,
            'performance': Factory.build_performances
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

    def build_artist(self, artist_data: dict) -> Artist:
        self.artist_count += 1
        return Artist(
            sk_id         = artist_data['id'],
            display_name  = artist_data['displayName'],
            uri           = artist_data['uri'],
            tour_end_date = artist_data['onTourUntil'] )


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


    def build_event(self, event_data: dict) -> Event:
        self.event_count += 1
        return Event(
            display_name = event_data['displayName'],
            event_type   = event_data['type'],
            location     = self.build_location(event_data['location']),
            performances = self.build_performances(event_data['performance']),
            popularity   = event_data['popularity'],
            sk_id        = event_data['id'],
            start        = event_data['start'],
            status       = event_data['status'],
            uri          = event_data['uri'],
            venue        = self.build_venue_by_id(int(event_data['venue']['id'])) if event_data['venue']['id'] else None)

    def concurrent_build_events(self, event_data: list):
        pass



    def build_location(self, location_data: dict) -> Location:
        self.location_count += 1
        return Location(
            city = location_data['city'],
            lat  = location_data['lat'],
            lng  = location_data['lng'])



    def build_metro_area(self, metro_area_data: dict) -> MetroArea:
        self.metro_count += 1
        return MetroArea(
            sk_id        = metro_area_data['id'],
            uri          = metro_area_data['uri'],
            display_name = metro_area_data['displayName'],
            country      = metro_area_data['country'])


    def build_performances(self, performance_data: [{}]) -> [Performance]:
        performance_list = []
        for performance in performance_data:
            self.performance_count += 1
            new_performance =  Performance(
                artist        = self.build_artist_by_name(performance['artist']['displayName']),
                billing       = performance['billing'],
                billing_index = performance['billingIndex'],
                name          = performance['displayName'],
                sk_id         = performance['id'])
            performance_list.append(new_performance)
        return performance_list


    def build_venue(self, venue_data: dict) -> Venue:
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


    def build_venue_by_id(self, venue_id: int) -> Venue:
        venue_data = Query.search_venue_by_id(venue_id)
        return self.build_venue(venue_data)

    def total_objects(self):
        return self.artist_count + self.performance_count + self.location_count + self.event_count + self.venue_count + self.metro_count







