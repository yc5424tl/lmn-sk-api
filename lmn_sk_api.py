import os

import multiprocessing
from flask_executor import Executor
import requests
from flask import Flask, request, jsonify

import config
import sk_api_mgr
import sk_factory
import pprint
import sk_query_mgr


class SkEvent(object):
    # def __init__(self,
    #              display_name: str,
    #              event_type:   str,
    #              # location:     Location or None,
    #              # performances: [Performance] or None,
    #              popularity:   float         or None,
    #              sk_id:        int,
    #              start:        dict,
    #              status:       str,
    #              uri:          str):
    #              # venue:        Venue):

    def __init__(self, event_data: dict):
        print(f'\nEVENT DATA -> \n\n{event_data}\n')
        # try:
        self.display_name = event_data['displayName']
        self.event_type = event_data['type']
        self.popularity = event_data['popularity']
        self.sk_id = event_data['id']
        self.start = event_data['start']
        self.status = event_data['status']
        self.uri = event_data['uri']
        print('end of __init__')
        # except Exception as exc:
        #     print(f'Exception {exc} building event')
            # self.display_name = display_name
            # self.event_type   = event_type
            # # self.location     = location
            # # self.performances = performances
            # self.popularity   = popularity
            # self.sk_id        = sk_id
            # self.start        = start
            # self.status       = status
            # self.uri          = uri
            # # self.venue        = venue

    def __str__(self) -> str:
        return self.display_name

        # return f'{", ".join([perf.__str__() for perf in self.performances])}'\
        #        f' @ {self.venue}' if self.venue else '' + f'{self.start}' if self.start else ''


    def __dict__(self):
        return {'display_name': self.display_name,
                'event_type'  : self.event_type,
                # 'location'    : self.location.__dict__(),
                # 'performances': [performance.__dict__() for performance in self.performances],
                'popularity'  : self.popularity,
                'sk_id'       : self.sk_id,
                'start'       : self.start,
                'status'      : self.status,
                'uri'         : self.uri}
                # 'venue'       : self.venue.__dict__() if self.venue else None}


# __name__ = 'lmn-sk-api.lmn_sk_api'

app = Flask(__name__)
app.config.from_object(config.Config)
executor = Executor(app)
# _pool = None
pp = pprint.PrettyPrinter()
factory = sk_factory.Factory()
API = sk_api_mgr.API()
log = sk_api_mgr.log
Query = sk_query_mgr.Query()
# session = None

# def set_global_session():
#     global session
#     if not session:
#         session = requests.Session()

# def get_local_event_data(ip):
#     local_event_data = API.search_events_near_ip(ip_addr=ip)
#     return local_event_data

def parallel_get_events(event_dict_list:[{}]):
    p = multiprocessing.Pool(processes=5)
    sk_events = p.map(SkEvent, [sk_event for sk_event in event_dict_list])
    print(f'sk_events = {sk_events}')
    p.close()
    p.join()
    return sk_events

@app.route('/events/local')
def local_events_response():
    # local_event_data = API.search_events_near_ip(ip_addr=request.access_route[-1])
    print(f'__name__ == {__name__}')

    if __name__ == 'lmn-sk-api.lmn_sk_api':
        multiprocessing.freeze_support()
        # api_result = Query.conc_search_events_by_ip_location(ip_addr=request.access_route[-1])
        api_result = Query.search_events_by_ip_location(request.access_route[-1])
        print('have api results to send')
        sk_events_list = parallel_get_events(api_result[0:3])
        print('past parallel_get_events')
        for ske in sk_events_list:
            print(f'type(ske) -> {type(ske)}')
            print(ske)
        return (jsonify([ske.__dict__() for ske in sk_events_list]), 200) if sk_events_list else (f'No Events Found Near IP Address {request.access_route[-1]}', 200)








    #     print('in if __name__....')
    #     sk_events_list = parallel_get_events(local_events_data)
    #     print('after sk_events_list = parallel_get_events(local_events_data)')
    #     for ske in sk_events_list:
    #         print(f'type(ske) -> {type(ske)}')
    #         print(ske)
    #     return (jsonify([event.__dict__() for event in sk_events_list]), 200) if sk_events_list else (f'No Events Found Near IP Address {request.access_route[-1]}', 200)
    # else:
    #     print(f'__name__ ==> {__name__}')
    #     return '__name__ not scoped', 200
    # result = (jsonify([event.__dict__() for event in local_event_data]), 200) if local_event_data \
    #     else (f'No Local Events For IP Address {request.access_route[-1]}', 200)



    # print(f'request.access_route[-1]: {request.access_route[-1]}')
    # print(f'type(request.access_route[-1]: {type(request.access_route[-1])}')
    # log(f'Local Events Request @ {request.access_route[-1]}')
    # # local_event_data = _pool.apply_async(get_local_event_data, [request.access_route[-1]])
    # # result = local_event_data.get()
    # # print('MULTIPROCESSING RESULT! ->')
    # # pp.pprint(result)
    #
    # # local_event_data = API.search_events_near_ip(request.access_route[-1], executor)
    # local_event_data = API.search_events_near_ip(ip_addr=request.access_route[-1])
    # print(f'\n\nLOCAL EVENT DATA\n{local_event_data}\nEND LOCAL EVENT DATA\n\n')
    # result = (jsonify([event.__dict__() for event in local_event_data]), 200) if local_event_data \
    #     else (f'No Local Events For IP Address {request.access_route[-1]}', 200)
    # print(f'Total # Objects Instantiated: {factory.total_objects()}')
    # return result

@app.route('/artist/gigography/<artist_id>')
def gigography_response(artist_id: int):
    log(f'Gigography Request for Artist ID {artist_id} @ {request.access_route[-1]}')
    event_data = API.search_artist_gigography(artist_id)
    return (jsonify([event.__dict__() for event in event_data]), 200) if event_data \
        else (f'No Gigography For Artist ID {artist_id}', 200)


@app.route('/artist/search/top/<artist_name>')
def artist_response(artist_name: str):
    log(f'Artist Request for {artist_name} @ {request.access_route[-1]}')
    artist_data = API.search_for_artist(artist_name, match_first=True)
    return (jsonify(artist_data.__dict__()), 200) if artist_data \
        else (f'No Artist Match Found For {artist_name}', 200)


@app.route('/artist/search/all/<artist_name>')
def artists_response(artist_name: str):
    log(f'Artists Request for {artist_name} @ {request.access_route[-1]}')
    artist_data = API.search_for_artist(artist_name=artist_name, match_first=False)
    return (jsonify([artist.__dict__() for artist in artist_data]) , 200) if artist_data \
        else (f'No Matching Artists for {artist_name}', 200)


@app.route('/events/artist/<artist_id>')
def artist_upcoming_response(artist_id: int):
    log(f'Artist Events Request for {artist_id} @ {request.access_route[-1]}')
    upcoming_data = API.search_artist_id_for_upcoming_events(artist_id)
    return (jsonify([event.__dict__() for event in upcoming_data]), 200) if upcoming_data \
        else (f'No Upcoming Events Found For Artist ID {artist_id}', 200)


@app.route('/venue/<venue_id>')
def venue_id_response(venue_id):
    log(f'Venue Request for ID {venue_id} @ {request.access_route[-1]}')
    venue_data = API.search_venue_id(venue_id)
    return (jsonify([venue.__dict__() for venue in venue_data]), 200) if venue_data \
        else (f'No Match Found for Venue ID {venue_id}', 200)


@app.route('/venue/search/all/<venue_name>')
def venues_response(venue_name):
    log(f'Venues Request for {venue_name} @ {request.access_route[-1]}')
    venue_data = API.search_venues(venue_name=venue_name, first_match=False)
    return (jsonify([venue.__dict__() for venue in venue_data]), 200) if venue_data \
        else (f'No Matches Found for {venue_name}', 200)


@app.route('/venue/search/top/<venue_name>')
def venue_response(venue_name):
    log(f'Venue Request for {venue_name} @ {request.access_route[-1]}')
    venue_data = API.search_venues(venue_name=venue_name, first_match=True)
    return (jsonify([venue.__dict__() for venue in venue_data]), 200) if venue_data \
        else (f'No Venues Matched For {venue_name}', 200)

@app.route('/events/venue/<venue_id>')
def venue_upcoming_response(venue_id: int):
    log(f'Venue Events Request for {venue_id} @ {request.access_route[-1]}')
    upcoming_data = API.search_venue_id_for_upcoming_events(venue_id)
    return (jsonify([event.__dict__() for event in upcoming_data]), 200) if upcoming_data \
        else (f'No Upcoming Events Found for Venue ID {venue_id}', 200)


@app.route('/events/metro_area/<metro_area_id>')
def metro_area_upcoming(metro_area_id: int):
    log(f'Metro Area Events Request for {metro_area_id} @ {request.access_route[-1]}')
    upcoming_data = API.search_events_by_metro_area(metro_area_id)
    return (jsonify([event.__dict__() for event in upcoming_data]), 200) if upcoming_data \
        else (f'No upcoming events found for Metro ID {metro_area_id}', 200)
# @app.route('/venue/<venue_name>')
# def venue_response(venue_name: str):
#     log(f'Venue Request for {venue_name} @ {request.access_route[-1]}')
#     api_data = API.search_venues(venue_name)
#     venue_dict_list = API.instantiate_venues_from_list(api_data)
#     serialized_venue_list = API.serialize_list(venue_dict_list)
#     return jsonify(serialized_venue_list), 200
#
#
# @app.route('/upcoming/artist/<int:sk_id>')
# def artist_upcoming_response(sk_id: int):
#     log(f'Artist Upcoming Request for {sk_id} @ {request.access_route[-1]}')
#     api_data = API.search_artist_id_for_upcoming_events(sk_id)
#     event_dict_list = API.instantiate_events_from_list(api_data)
#     serialized_event_list = API.serialize_list(event_dict_list)
#     return jsonify(serialized_event_list), 200
#
#
# @app.route('/upcoming/venue/<int:venue_id>')
# def venue_upcoming_response(venue_id: int):
#     log(f'Venue Upcoming Request for {venue_id} @ {request.access_route[-1]}')
#     api_data = API.search_venue_id_for_upcoming_events(venue_id)
#     event_dict_list = API.instantiate_events_from_list(api_data)
#     serialized_event_list = API.serialize_list(event_dict_list)
#     return jsonify(serialized_event_list), 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# if __name__ == '__main__':
#     _pool = multiprocessing.Pool(processes=4)
#     port = int(os.environ.get("PORT", 5000))
#     try:
#         app.run(host='0.0.0.0', port=port)
#     except KeyboardInterrupt:
#         _pool.close()
#         _pool.join()
