import concurrent.futures
import multiprocessing
import requests
import time
from flask import Flask, request, jsonify
import config
import os

class SkEvent:
    def __init__(self, event_data: dict):
                 self.display_name = event_data['displayName']
                 self.event_type   = event_data['type']
                 self.popularity   = event_data['popularity']
                 self.sk_id        = event_data['id']
                 self.start        = event_data['start']
                 self.status       = event_data['status']
                 self.uri          = event_data['uri']

    def __str__(self):
        return self.display_name

    def __dict__(self):
        return {'display_name': self.display_name,
                'event_type': self.event_type,
                'popularity': self.popularity,
                'sk_id': self.sk_id,
                'start': self.start,
                'status': self.status,
                'uri': self.uri}


def parallel_build_events(event_data):
    p = multiprocessing.Pool(processes=5)
    sk_events = p.map(SkEvent, [sk_event for sk_event in event_data])
    p.close()
    p.join()
    return sk_events


def concurrent_paginate_api_result(page_num):
    result_page = requests.get(f"https://api.songkick.com/api/3.0/events.json?apikey={os.getenv('SK_API_KEY')}&location=ip:67.220.22.82", params={'page': page_num}).json()
    page_events = []
    try:
        for event in result_page['resultsPage']['results']['event']:
            page_events.append(event)
    except KeyError as kE:
        if 'clientLocation' in result_page['resultsPage'].keys():
            print('clientLocation in response_page')
        else:
            print(f'Key Error: {kE} processing page {page_num}')
    return page_events



if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = Flask(__name__)
    app.config.from_object(config.Config)

    @app.route('/events/local')
    def local_events_response():
        ip = '67.220.22.82'
        api_result = requests.get(f"https://api.songkick.com/api/3.0/events.json?apikey={os.getenv('SK_API_KEY')}&location=ip:{ip}").json()
        event_dict_list = api_result['resultsPage']['results']['event']
        object_count = api_result['resultsPage']['totalEntries']
        api_result_page_count = round(object_count/50) -1
        event_dicts = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
            future_to_event = [executor.submit(concurrent_paginate_api_result, page_num) for page_num in range(2, api_result_page_count+1)]
            for future in concurrent.futures.as_completed(future_to_event):
                try:
                    data = future.result()
                    for event in data:
                        event_dicts.append(event)
                except Exception as exc:
                    print(f'exception {exc}')
            event_dict_list.extend(event_dicts)
        time.sleep(seconds=15)
        print(f'len(event_dict_list) -> {len(event_dict_list)}')
        test_event_data = event_dict_list[0:3]
        sk_event_objects = parallel_build_events(test_event_data)
        for ske in sk_event_objects:
            print(f'type(ske) -> {type(ske)}')
            print(ske)
        return jsonify([ske.__dict__() for ske in sk_event_objects], 200)

