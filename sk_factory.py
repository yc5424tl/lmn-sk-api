from api_models.sk_metro_area import MetroArea
from sk_query_mgr import Query
from api_models.sk_artist import Artist
from api_models.sk_city import City
from api_models.sk_event import Event
from api_models.sk_location import Location
from api_models.sk_performance import Performance
from api_models.sk_venue import Venue

Query = Query()


# class Factory(object):

def instance_call(list_data: [{}], class_call):
    if not bool(len(list_data)):
        return []
    else:
        switcher = {
            Artist: build_artist,
            City: build_city,
            Event: build_event,
            Location: build_location,
            Venue: build_venue,
            MetroArea: build_metro_area,
            Performance: build_performances
        }
        function_call = switcher.get(class_call)

        return function_call(list_data)



def build_artist(artist_data: dict) -> Artist:
    return Artist(
        sk_id         = artist_data['id'],
        display_name  = artist_data['displayName'],
        uri           = artist_data['uri'],
        tour_end_date = artist_data['onTourUntil'] )


def build_artist_by_name(artist_name: str) -> Artist:
    artist_dict = Query.search_artists_by_name(artist_name, match_first=True)
    new_artist = build_artist(artist_dict)
    return new_artist



def build_city(city_data: dict) -> City:
    return City(
        sk_id   = city_data['id'],
        name    = city_data['displayName'],
        uri     = city_data['uri'],
        country = city_data['country'])


def build_event(event_data: dict) -> Event:
    return Event(
        display_name = event_data['displayName'],
        event_type   = event_data['type'],
        location     = build_location(event_data['location']),
        performances = build_performances(event_data['performance']),
        popularity   = event_data['popularity'],
        sk_id        = event_data['id'],
        start        = event_data['start'],
        status       = event_data['status'],
        uri          = event_data['uri'],
        venue        = build_venue_by_id(int(event_data['venue']['id'])) if event_data['venue']['id'] else None)



def build_location(location_data: dict) -> Location:
    return Location(
        city = location_data['city'],
        lat  = location_data['lat'],
        lng  = location_data['lng'])



def build_metro_area(metro_area_data: dict) -> MetroArea:
    return MetroArea(
        sk_id        = metro_area_data['id'],
        uri          = metro_area_data['uri'],
        display_name = metro_area_data['displayName'],
        country      = metro_area_data['country'])


def build_performances(performance_data: [{}]) -> [Performance]:
    performance_list = []
    for performance in performance_data:
        new_performance =  Performance(
            artist        = build_artist_by_name(performance['artist']['displayName']),
            billing       = performance['billing'],
            billing_index = performance['billingIndex'],
            name          = performance['displayName'],
            sk_id         = performance['id'])
        performance_list.append(new_performance)
    return performance_list


def build_venue(venue_data: dict) -> Venue:
    return Venue(
        capacity    = venue_data['capacity'],
        city        = venue_data['city'],
        description = venue_data['description'],
        lat         = venue_data['lat'],
        lng         = venue_data['lng'],
        metro_area  = build_metro_area(venue_data['metroArea']),
        name        = venue_data['displayName'],
        phone       = venue_data['phone'],
        sk_id       = venue_data['id'],
        street      = venue_data['street'],
        uri         = venue_data['uri'],
        website     = venue_data['website'],
        zip_code    = venue_data['zip'])


def build_venue_by_id(venue_id: int) -> Venue:
    venue_data = Query.search_venue_by_id(venue_id)
    return build_venue(venue_data)







