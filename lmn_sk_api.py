import os

from flask import Flask, request, jsonify
import config
from sk_api_mgr import API, log

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
API = API()


@app.route('/events')
def local_events_response():
    log(f'Local Events Request @ {request.access_route[-1]}')
    api_data = API.search_events_near_ip(request.access_route[-1])
    return jsonify(local_events=[Event.__dict__() for Event in api_data]), 200


@app.route('/artist/search/first/<artist_name>')
def artist_response(artist_name: str):
    log(f'Artist Request for {artist_name} @ {request.access_route[-1]}')
    artist_data = API.search_for_artist(artist_name, match_first=True)
    return (jsonify(artist_data.to_dict()),200) if artist_data else (f'Match not Found For {artist_name}',200)


@app.route('/artist/search/all/<artist_name>')
def matching_artists_response(artist_name: str):
    log(f'Matching Artists Request for {artist_name} @ {request.access_route[-1]}')
    artist_data = API.search_for_artist(artist_name=artist_name, match_first=False)
    return (jsonify({artist.display_name:artist.to_dict() for artist in artist_data}) , 200) if artist_data \
        else (f'No Matches for {artist_name}', 200)




@app.route('/venue/<venue_name>')
def venue_response(venue_name: str):
    log(f'Venue Request for {venue_name} @ {request.access_route[-1]}')
    api_data = API.search_venues(venue_name)
    venue_dict_list = API.instantiate_venues_from_list(api_data)
    serialized_venue_list = API.serialize_list(venue_dict_list)
    return jsonify(serialized_venue_list), 200


@app.route('/upcoming/artist/<int:sk_id>')
def artist_upcoming_response(sk_id: int):
    log(f'Artist Upcoming Request for {sk_id} @ {request.access_route[-1]}')
    api_data = API.search_artist_id_for_upcoming_events(sk_id)
    event_dict_list = API.instantiate_events_from_list(api_data)
    serialized_event_list = API.serialize_list(event_dict_list)
    return jsonify(serialized_event_list), 200


@app.route('/upcoming/venue/<int:venue_id>')
def venue_upcoming_response(venue_id: int):
    log(f'Venue Upcoming Request for {venue_id} @ {request.access_route[-1]}')
    api_data = API.search_venue_id_for_upcoming_events(venue_id)
    event_dict_list = API.instantiate_events_from_list(api_data)
    serialized_event_list = API.serialize_list(event_dict_list)
    return jsonify(serialized_event_list), 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
