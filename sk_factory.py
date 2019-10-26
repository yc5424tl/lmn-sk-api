from api_models.sk_metro_area import MetroArea
from api_models.sk_artist import Artist
from api_models.sk_city import City
from api_models.sk_event import Event
from api_models.sk_location import Location
from api_models.sk_performance import Performance
from api_models.sk_simplified_venue import SimplifiedVenue
from api_models.sk_venue import Venue
import logging

log = logging.getLogger()

class Factory(object):

    def __init__(self):
        self.event_count       = 0
        self.venue_count       = 0
        self.location_count    = 0
        self.artist_count      = 0
        self.performance_count = 0
        self.city_count        = 0
        self.metro_count       = 0



    def build_artist(self, artist_data: dict) -> Artist or None:
        try:
            new_artist = Artist(
                display_name  = artist_data['displayName'],
                uri           = artist_data['uri'],
                sk_id         = artist_data['id'])
            self.artist_count += 1
            return new_artist
        except Exception as exc:
            log.log(msg=f'Exception {exc} building artist with: {artist_data}', level=Warning)
            return None



    def build_city(self, city_data: dict) -> City or None:
        try:
            new_city = City(
                country      = city_data['country']['displayName'],
                display_name = city_data['displayName'],
                sk_id        = city_data['id'],
                uri          = city_data['uri'])
            self.city_count += 1
            return new_city
        except Exception as exc:
            log.log(msg=f'Exception {exc} building city with: {city_data}', level=Warning)
            return None



    def build_event(self, event_data: dict) -> Event or None:
        try:
            event_location  = self.build_location(event_data['location'])
            event_venue     = self.build_simplified_venue(event_data['venue'])
            # event_perf_list = self.build_performances(event_data['performance'])
            new_event = Event(
                display_name = event_data['displayName'],
                event_type   = event_data['type'],
                location     = event_location,
                # performance  = event_perf_list,
                popularity   = event_data['popularity'],
                sk_id        = event_data['id'],
                start        = event_data['start'],
                status       = event_data['status'],
                uri          = event_data['uri'],
                venue        = event_venue)
            self.event_count += 1
            return new_event
        except Exception as exc:
            log.log(msg=f'Exception {exc} building event', level=Warning)
            return None



    def build_location(self, location_data: dict) -> Location or None:
        try:
            new_location = Location(
                city = location_data['city'],
                lat  = location_data['lat'],
                lng  = location_data['lng'])
            self.location_count += 1
            return new_location
        except Exception as exc:
            log.log(msg=f'Exception {exc} building location with: {location_data}', level=Warning)
            return None



    def build_metro_area(self, metro_area_data: dict) -> MetroArea or None:
        try:
            new_metro_area =  MetroArea(
                sk_id        = metro_area_data['id'],
                uri          = metro_area_data['uri'],
                display_name = metro_area_data['displayName'],
                country      = metro_area_data['country'])
            self.metro_count += 1
            return new_metro_area
        except Exception as exc:
            log.log(msg=f'Exception {exc} building metro area with: {metro_area_data}', level=Warning)
            return None



    def build_performances(self, performance_data: [{}]) -> [Performance]:
        performance_list = []
        for performance in performance_data:
            try:
                new_performance =  Performance(
                        artist        = self.build_artist(performance_data['artist']),
                        billing       = performance['billing'],
                        billing_index = performance['billingIndex'],
                        display_name  = performance['displayName'],
                        sk_id         = performance['id'])
                performance_list.append(new_performance)
                self.performance_count += 1
            except Exception as exc:
                log.log(msg=f'Exception {exc} building performance with: {performance}', level=Warning)
                pass
        return performance_list



    def build_simplified_venue(self, simp_venue_data: dict) -> SimplifiedVenue or None:
        try:
            new_simplified_venue = SimplifiedVenue(
                display_name = simp_venue_data['displayName'],
                sk_id        = simp_venue_data['id'],
                uri          = simp_venue_data['uri'],
                metro_area   = simp_venue_data['metroArea'] if simp_venue_data['metroArea'] else None)
            self.venue_count += 1
            return new_simplified_venue
        except Exception as exc:
            log.log(msg=f'Exception {exc} building simplified venue with {simp_venue_data}', level=Warning)
            return None



    def build_venue(self, venue_data: dict) -> Venue or None:
        description    = venue_data['description'] if venue_data.keys().__contains__('description') else None
        lat            = venue_data['lat']         if venue_data.keys().__contains__('lat')         else None
        lng            = venue_data['lng']         if venue_data.keys().__contains__('lng')         else None
        phone          = venue_data['phone']       if venue_data.keys().__contains__('phone')       else None
        street         = venue_data['street']      if venue_data.keys().__contains__('street')      else None
        venue_capacity = venue_data['capacity']    if venue_data.keys().__contains__('capacity')    else 0
        website        = venue_data['website']     if venue_data.keys().__contains__('website')     else None
        zip_code       = venue_data['zip']         if venue_data.keys().__contains__('zip')         else None

        new_location = None
        if venue_data.keys().__contains__('city'):
            new_location = Location(city=venue_data['city'], lng=lng, lat=lat)
        elif venue_data.keys().__contains__('location'):
            if venue_data['location'].keys().__contains__('city'):
                new_location = Location(city=venue_data['location']['city'], lng=lng, lat=lat)

        try:
            new_venue = Venue(
                capacity     = venue_capacity,
                description  = description,
                display_name = venue_data['displayName'],
                location     = new_location,
                phone_num    = phone,
                sk_id        = venue_data['id'],
                street       = street,
                uri          = venue_data['uri'],
                website      = website,
                zip_code     = zip_code)
            self.venue_count += 1
            return new_venue
        except Exception as exc:
            log.log(msg=f'Exception {exc} building Venue with: {venue_data}', level=Warning)
            return None


    @property
    def total_objects(self):
        return self.artist_count + self.performance_count + self.location_count + \
               self.event_count + self.venue_count + self.metro_count







