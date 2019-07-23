import os

from flask import Flask, request, jsonify
import config
from sk_api_mgr import API, log
# from api_models.sk_artist import Artist
# from api_models.sk_event import Event
# from api_models.sk_venue import Venue
app = Flask(__name__)
cfg = config.DevelopmentConfig
app.config.from_object(cfg)
API = API()


@app.route('/events/local')
def local_events_response():
    log(f'Local Events Request @ {request.access_route[-1]}')
    event_data = API.search_events_near_ip(request.access_route[-1])
    return (jsonify(local_events={Event.__dict__() for Event in event_data}), 200) if event_data \
        else (jsonify({None: f'No Events Found Near {request.access_route[-1]}'}), 200)


@app.route('/artist/search/first/<string:artist_name>')
def artist_response(artist_name: str):
    log(f'Artist Request for {artist_name} @ {request.access_route[-1]}')
    artist_data = API.search_artists(artist_name, match_first=True)
    return (jsonify(artist=artist_data.__dict__()), 200) if artist_data \
        else (jsonify(artist={None: f'Match not Found For: {artist_name}'}), 200)


@app.route('/artist/search/all/<string:artist_name>')
def artists_response(artist_name: str):
    log(f'Artists Request for {artist_name} @ {request.access_route[-1]}')
    artist_data = API.search_artists(artist_name=artist_name, match_first=False)
    return (jsonify({Artist.__dict__() for Artist in artist_data}), 200) if artist_data \
        else (jsonify(artists=f'No Artists Found For: {artist_name}'), 200)


@app.route('/artist/upcoming/<artist_id>')
def artist_upcoming_response(artist_id: int):
    log(f'Artist Upcoming Request for {artist_id} @ {request.access_route[-1]}')
    upcoming_data = API.search_artist_id_for_upcoming_events(artist_id)
    print(f' UPCOMING_DATA TYPE = {type(upcoming_data)}')
    for Event in upcoming_data:
        print(f'EVENT IN UPCOMING_DATA TYPE = {type(Event)}')
    return (jsonify(upcoming_events={Event.__dict__() for Event in upcoming_data}), 200) if upcoming_data \
        else (jsonify(upcoming_events={None: f'No Upcoming Events Found For Artist {artist_id}'}), 200)


@app.route('/venue/search/all/<string:venue_name>')
def venues_response(venue_name: str):
    log(f'Venues Request for {venue_name} @ {request.access_route[-1]}')
    venue_data = API.search_venues(venue_name=venue_name, match_first=False)
    return (jsonify(venues={Venue.__dict__() for Venue in venue_data}), 200) if venue_data \
        else (jsonify(venues={None: f'No Venues Found For: {venue_name}'}), 200)


@app.route('/venue/search/first/<string:venue_name>')
def venue_response(venue_name: str):
    log(f'Venue Request for {venue_name} @ {request.access_route[-1]}')
    venue_data = API.search_venues(venue_name=venue_name, match_first=True)
    return (jsonify(venue=venue_data.__dict__()), 200) if venue_data \
        else (jsonify(venue={None: f'No Venue Found For {venue_name}'}), 200)


@app.route('/venue/upcoming/<int:venue_id>')
def venue_upcoming_response(venue_id: int):
    log(f'Venue Upcoming Request for {venue_id} @ {request.access_route[-1]}')
    upcoming_data = API.search_venue_id_for_upcoming_events(venue_id, match_first=False)
    return (jsonify(upcoming_events={Event.__dict__() for Event in upcoming_data}), 200) if upcoming_data \
        else (jsonify(upcoming_events={None: f'No Upcoming Events Found For Venue {venue_id}'}), 200)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
