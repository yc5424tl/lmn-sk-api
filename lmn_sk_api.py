import concurrent.futures
import json
import os
import pprint

import requests
from flask import Flask, request, Response

import config
import controller
from controller import factory

app = Flask(__name__)
app.config.from_object(config.Config)
pp=pprint.PrettyPrinter()

artist_events_url = "https://api.songkick.com/api/3.0/artists/{query}/calendar.json?apikey={key}"
artists_url = "https://api.songkick.com/api/3.0/search/artists.json?apikey={key}&query={query}"
gigography_url = "https://api.songkick.com/api/3.0/artists/{query}/gigography.json?apikey={key}"
ip_events_url = "https://api.songkick.com/api/3.0/events.json?apikey={key}&location=ip:{query}"
key = os.getenv('SK_API_KEY')
metro_area_events_url = "https://api.songkick.com/api/3.0/metro_areas/{query}/calendar.json?apikey={key}"
venue_events_url = "https://api.songkick.com/api/3.0/venues/{query}/calendar.json?apikey={key}"
venue_id_url = "https://api.songkick.com/api/3.0/venues/{query}.json?apikey={key}"
venues_url = "https://api.songkick.com/api/3.0/search/venues.json?query={query}&apikey={key}"



def generate(data_list: [{}], call: str):
    instances = 0
    try:
        prev = next(iter(data_list))
    except StopIteration:
        yield "{" + f'{call}s: []'
        raise StopIteration
    yield "{" + f'{call}s: ['
    for data in data_list:
        if isinstance(data, list):
            pass
        else:
            instances += 1
            print(f'COUNT:{instances}  TYPE:{type(data)} OBJECT: {data})')
            yield json.dumps(data.__dict__(), sort_keys=True, indent=4) + ', '
            prev = data
    yield json.dumps(prev.__dict__()) + ']}'


@app.route('/events/local')
def get_local_events():
    # NYC ip_addr = '104.131.241.43' if request.access_route[-1] == '127.0.0.1' else request.access_route[-1]
    ip_addr = '67.220.22.82' if request.access_route[-1] == '127.0.0.1' else request.access_route[-1]
    return get_query(endpoint=ip_events_url, argument=ip_addr, call='event')


@app.route('/artist/gigography/<artist_id>')
def get_gigography(artist_id: int):
    return get_query(endpoint=gigography_url, argument=artist_id, call='event')


@app.route('/artist/search/top/<artist_name>')
def get_artist(artist_name: str):
    return get_query(endpoint=artists_url, argument=artist_name, call='artist', match_first=True)


@app.route('/artist/search/all/<artist_name>')
def get_artists(artist_name: str):
    return get_query(endpoint=artists_url, argument=artist_name, call='artist')


@app.route('/events/artist/<artist_id>')
def get_artist_events(artist_id):
    return get_query(endpoint=artist_events_url, argument=artist_id, call='event')


@app.route('/venue/<venue_id>')
def get_venue_id(venue_id):
    return get_query(endpoint=venue_id_url, argument=venue_id, call='venue')


@app.route('/venue/search/all/<venue_name>')
def get_venues(venue_name: str):
    return get_query(endpoint=venues_url, argument=venue_name, call='venue')


@app.route('/venue/search/top/<venue_name>')
def get_venue(venue_name: str):
    return get_query(endpoint=venues_url, argument=venue_name, call='venue', match_first=True)


@app.route('/events/venue/<venue_id>')
def get_venue_events(venue_id: int):
    return get_query(endpoint=venue_events_url, argument=venue_id, call='event')


@app.route('/events/metro_area/<metro_area_id>')
def get_metro_area_events(metro_area_id: int):
    return get_query(endpoint=metro_area_events_url, argument=metro_area_id, call='event')


def get_query(endpoint: str, argument: str or int, call: str, match_first=False):
    data = concurrent_query(endpoint=endpoint, argument=argument, call=call, match_first=match_first)
    if isinstance(data, type(None)):
        return Response(json.dumps({'response': []}), content_type='application.json')
    else:
        instance_list = controller.instantiate_list_data(list_data=data, call=call)
        return Response(generate(instance_list, call), content_type='application.json')


def concurrent_pagination(page_num: int, argument: str, endpoint: str, call: str):
    response = requests.get(endpoint.format(query=argument, key=key), params={'page': page_num}).json()
    page_data = []
    try:
        for attr_dict in response['resultsPage']['results'][call]:
            page_data.append(attr_dict)
    except KeyError as kE:
        if 'clientLocation' in response['resultsPage'].keys():
            controller.log.log(f'clientLocation in response, page {page_num}')
            pass
        else:
            controller.log.log(f'KeyError: {kE} processing Page {page_num}')
    return page_data


def concurrent_query(endpoint: str, call: str, argument=None, match_first=False):
    response_data = requests.get(endpoint.format(query=argument, key=key)).json()
    try:
        dict_list = response_data['resultsPage']['results'][call]
        if 'totalEntries' in response_data['resultsPage'].keys():
            object_count = response_data['resultsPage']['totalEntries']
            if object_count == 0:
                return [{'objects': 'None Found'}]
            num_pages = object_count // 50
            partial_page = object_count % 50
            if partial_page > 0:
                num_pages += 1
        else:
            num_pages = 1
        if match_first:
            dict_list = dict_list[0]
        data_dicts = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
            futures_to_data = \
                [executor.submit(concurrent_pagination, page_num=page, argument=argument, endpoint=endpoint, call=call) for page in range(2, num_pages + 1)]
            for future in concurrent.futures.as_completed(futures_to_data):
                try:
                    data = future.result()
                    for attr_dict in data:
                        data_dicts.append(attr_dict)
                except Exception as exc:
                    controller.log.log(f'Exception {exc} in concurrent_query')
                else:
                    pass
            dict_list.extend(data_dicts)
            return dict_list
    except KeyError as kE:
        controller.log.log(f'KeyError {kE} in concurrent_query')
        return None

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
