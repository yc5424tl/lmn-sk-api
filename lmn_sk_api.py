import os

from flask import Flask, request, jsonify
import config
from sk_api_mgr import API, log

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
API = API()

import pprint
pp = pprint.PrettyPrinter()


@app.route('/events/local')
def local_events_response():
    log(f'Local Events Request @ {request.access_route[-1]}')
    local_event_data = API.search_events_near_ip(request.access_route[-1])
    return jsonify(local_events=[event.__dict__() for event in local_event_data]), 200 if local_event_data \
        else f'No Local Events For IP Address {request.access_route[-1]}', 200


@app.route('/artist/gigography/<artist_id>')
def gigography_response(artist_id: int):
    log(f'Gigography Request for Artist ID {artist_id} @ {request.access_route[-1]}')
    event_data = API.search_artist_gigography(artist_id)
    return jsonify(gigography=[event.__dict__() for event in event_data]), 200 if event_data \
        else f'No Gigography For Artist ID {artist_id}', 200


@app.route('/artist/search/top/<artist_name>')
def artist_response(artist_name: str):
    log(f'Artist Request for {artist_name} @ {request.access_route[-1]}')
    artist_data = API.search_for_artist(artist_name, match_first=True)
    return jsonify(artist=artist_data.__dict__()),200 if artist_data \
        else f'No Artist Match Found For {artist_name}',200


@app.route('/artist/search/all/<artist_name>')
def artists_response(artist_name: str):
    log(f'Artists Request for {artist_name} @ {request.access_route[-1]}')
    artist_data = API.search_for_artist(artist_name=artist_name, match_first=False)
    return jsonify(artists={artist.__dict__() for artist in artist_data}) , 200 if artist_data \
        else f'No Matching Artists for {artist_name}', 200


@app.route('/events/artist/<artist_id>')
def artist_upcoming_response(artist_id: int):
    log(f'Artist Events Request for {artist_id} @ {request.access_route[-1]}')
    upcoming_data = API.search_artist_id_for_upcoming_events(artist_id)
    return jsonify(events=[event.__dict__() for event in upcoming_data]), 200 if upcoming_data \
        else f'No Upcoming Events Found For Artist ID {artist_id}', 200


@app.route('/venue/<venue_id>')
def venue_id_response(venue_id):
    log(f'Venue Request for ID {venue_id} @ {request.access_route[-1]}')
    venue_data = API.search_venue_id(venue_id)
    return jsonify(venue=[venue.__dict__() for venue in venue_data]), 200 if venue_data \
        else f'No Match Found for Venue ID {venue_id}', 200


@app.route('/venue/search/all/<venue_name>')
def venues_response(venue_name):
    log(f'Venues Request for {venue_name} @ {request.access_route[-1]}')
    venue_data = API.search_venues(venue_name=venue_name, first_match=False)
    return jsonify(venues=[venue.__dict__() for venue in venue_data]), 200 if venue_data \
        else f'No Matches Found for {venue_name}', 200


@app.route('/venue/search/top/<venue_name>')
def venue_response(venue_name):
    log(f'Venue Request for {venue_name} @ {request.access_route[-1]}')
    venue_data = API.search_venues(venue_name=venue_name, first_match=True)
    return jsonify(venue=[venue.__dict__() for venue in venue_data]), 200 if venue_data \
        else f'No Venues Matched For {venue_name}', 200

@app.route('/events/venue/<venue_id>')
def venue_upcoming_response(venue_id: int):
    log(f'Venue Events Request for {venue_id} @ {request.access_route[-1]}')
    upcoming_data = API.search_venue_id_for_upcoming_events(venue_id)
    return jsonify(events=[event.__dict__() for event in upcoming_data]), 200 if upcoming_data \
        else f'No Upcoming Events Found for Venue ID {venue_id}', 200


@app.route('/events/metro_area/<metro_area_id>')
def metro_area_upcoming(metro_area_id: int):
    log(f'Metro Area Events Request for {metro_area_id} @ {request.access_route[-1]}')
    upcoming_data = API.search_events_by_metro_area(metro_area_id)
    return jsonify(events=[event.__dict__() for event in upcoming_data]), 200 if upcoming_data \
        else f'No upcoming events found for Metro ID {metro_area_id}', 200
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
