from multiprocessing import Pool, Process, current_process
import multiprocessing

class Event(object):
    def __init__(self,
                 display_name: str,
                 event_type:   str,
                 # location:     Location or None,
                 # performances: [Performance] or None,
                 popularity:   float         or None,
                 sk_id:        int,
                 start:        dict,
                 status:       str,
                 uri:          str):
                 # venue:        Venue):

        self.display_name = display_name
        self.event_type   = event_type
        # self.location     = location
        # self.performances = performances
        self.popularity   = popularity
        self.sk_id        = sk_id
        self.start        = start
        self.status       = status
        self.uri          = uri
        # self.venue        = venue

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


def worker(in_put, output):
    for func, args in iter(input.get, 'STOP'):
        result = calculate(func, args)
        output.put(result)

def calculate(func, args):
    result = func(*args)
    return '%s says that %s%s = %s' % (current_process().name, func.__name__, args, result)

class SkEvent(object):
    def __init__(self, event_data: dict):
        self.display_name=event_data['displayName']
        self.event_type=event_data['type']
        self.popularity=event_data['popularity']
        self.sk_id=event_data['id']
        self.start=event_data['start']
        self.status=event_data['status']
        self.uri=event_data['uri']

    def __str__(self):
        return f'{self.display_name} is a {self.event_type} starting at {self.start["time"]} on {self.start["date"]} w/ a popularity rating of {self.popularity}'

def build_event(event_dict: dict) -> Event or None:
    print(event_dict['displayName'])
    print(event_dict['type'])
    print(event_dict['popularity'])
    print(event_dict['id'])
    print(event_dict['start'])
    print(event_dict['status'])
    print(event_dict['uri'])

    event = Event(
        display_name=event_dict['displayName'],
        event_type=event_dict['type'],
        popularity=event_dict['popularity'],
        sk_id=event_dict['id'],
        start=event_dict['start'],
        status=event_dict['status'],
        uri=event_dict['uri'])
    return event

def build_event_star(args):
    return build_event(*args)



def parallel_get_events(event_dict_list:[{}]):
    p = multiprocessing.Pool(processes=5)
    sk_events = p.map(SkEvent, [sk_event for sk_event in event_dict_list])
    p.close()
    p.join()
    return sk_events



def test():
    event_data = [
        {'id': 38830059, 'displayName': 'Aaron Lewis at Mystic Lake Casino Hotel (November 16, 2019)', 'type': 'Concert', 'uri': 'http://www.songkick.com/concerts/38830059-aaron-lewis-at-mystic-lake-casino-hotel?utm_source=47812&utm_medium=partner',
'status': 'ok', 'popularity': 0.021507, 'start': {'date': '2019-11-16', 'datetime': '2019-11-16T20:00:00-0600', 'time': '20:00:00'}, 'performance': [{'id': 73576549, 'displayName': 'Aaron Lewis', 'billing': 'headline', 'billingIndex': 1, 'artist': {'id': 89047, 'displayName': 'Aaron Lewis', 'uri': 'http://www.songkick.com/artists/89047-aaron-lewis?utm_source=47812&utm_medium=partner', 'identifier': [{'mbid': 'c0d7ce5f-5602-4dec-a43b-ed3ee69a410f', 'href': 'http://api.songkick.com/api/3.0/artists/mbid:c0d7ce5f-5602-4dec-a43b-ed3ee69a410f.json'}, {'mbid': '86034d1d-f66e-426d-ad52-ca5511a9b428', 'href': 'http://api.songkick.com/api/3.0/artists/mbid:86034d1d-f66e-426d-ad52-ca5511a9b428.json'}]}}], 'ageRestriction': None, 'flaggedAsEnded': False, 'venue': {'id': 530, 'displayName': 'Mystic Lake Casino Hotel', 'uri': 'http://www.songkick.com/venues/530-mystic-lake-casino-hotel?utm_source=47812&utm_medium=partner', 'metroArea': {'displayName': 'Twin Cities', 'country': {'displayName': 'US'}, 'state': {'displayName': 'MN'}, 'id': 35130, 'uri': 'http://www.songkick.com/metro_areas/35130-us-twin-cities?utm_source=47812&utm_medium=partner'
}, 'lat': 44.72963, 'lng': -93.47499}, 'location': {'city': 'Prior Lake, MN, US', 'lat': 44.72963, 'lng': -93.47499}}, {'id': 39014003, 'displayName': 'The Outlaws and Atlanta Rhythm Sectionat Medina Entertainment Center (November 16, 2019)', 'type': 'Concert', 'uri': 'http://www.songkick.com/concerts/39014003-outlaws-at-medina-entertainment-center?utm_source=47812&utm_medium=partner', 'status': 'ok', 'popularity': 0.011171, 'start': {'date': '2019-11-16', 'datetime': '2019-11-16T19:30:0-0600', 'time': '19:30:00'}, 'performance': [{'id': 73894160, 'displayName': 'The Outlaws', 'billing': 'headline', 'billingIndex': 1, 'artist': {'id': 115093, 'displayName': 'The Outlaws', 'uri': 'http://www.songkick.com/artists/115093-outlaws?utm_source=47812&utm_medium=partner', 'identifier': [{'mbid': 'f33ea451-53c8-4d48-afc7-3e5857f01d42', 'href': 'http://api.songkick.com/api/3.0/artists/mbid:f33ea451-53c8-4d48-afc7-3e5857f01d42.json'}, {'mbid': 'a25b9b2c-bb90-4a27-8a1a-33457026cd86', 'href': 'http://api.songkick.com/api/3.0/artists/mbid:a25b9b2c-bb90-4a27-8a1a-33457026cd86.json'}, {'mbid': '6435afaf-0d34-4178-b9d4-0c60916f97a4', 'href': 'http://api.songkick.com/api/3.0/artists/mbid:6435afaf-0d34-4178-b9d4-0c60916f97a4.json'}, {'mbid': '16f0cc43-269a-4981-bcc0-da3d0981ed6d', 'href': 'http://api.songkick.com/api/3.0/artists/mbid:16f0cc43-269a-4981-bcc0-da3d0981ed6d.json'}, {'mbid': 'e1a01561-204f-49aa-8e9d-12d5d39564e1', 'href': 'http://api.songkick.com/api/3.0/artists/mbid:e1a01561-204f-49aa-8e9d-12d5d39564e1.json'
}]}}, {'id': 73894161, 'displayName': 'Atlanta Rhythm Section', 'billing': 'headline', 'billingIndex': 2, 'artist': {'id': 15731, 'displayName': 'Atlanta Rhythm Section', 'uri': 'http://www.songkick.com/artists/15731-atlanta-rhythm-section?utm_source=47812&utm_medium=partner', 'identifier': [{'mbid': '6b627bd0-b839-40c7-b025-7b60c122dfea', 'href': 'http://api.songkick.com/api/3.0/artists/mbid:6b627bd0-b839-40c7-b025-7b60c122dfea.json'}]}}], 'ageRestriction': None, 'flaggedAsEnded': False, 'venue': {'id': 66015, 'displayName': 'Medina Entertainment Center', 'uri': 'http://www.songkick.com/venues/66015-medina-entertainment-center?utm_source=47812&utm_medium=partner', 'metroArea': {'displayName': 'Twin Cities', 'country': {'displayName': 'US'}, 'state': {'displayName': 'MN'}, 'id': 35130, 'uri': 'http://www.songkick.com/metro_areas/35130-us-twin-cities?utm_source=47812&utm_medium=partner'}, 'lat': 45.04549, 'lng': -93.53446}, 'location': {'city': 'Medina, MN, US', 'lat': 45.04549, 'lng': -93.53446}}, {'id': 38754839, 'displayName': 'Candlebox at The Cabooze (November 16, 2019)', 'type': 'Concert', 'uri': 'http://www.songkick.com/concerts/38754839-candlebox-at-cabooze?utm_source=47812&utm_medium=partner', 'status': 'ok', 'popularity': 0.031634, 'start': {'date': '2019-11-16', 'datetime': '2019-11-16T19:00:00-0600', 'time': '19:00:00'}, 'performance': [{'id': 73445524, 'displayName': 'Candlebox', 'billing': 'headline', 'billingIndex': 1, 'artist': {'id': 238974, 'displayName': 'Candlebox', 'uri': 'http://www.songkick.com/artists/238974-candlebox?utm_source=47812&utm_medium=partner', 'identifier': [{'mbid': '8e9516ba-f417-47dd-a8a5-8998b94553f8', 'href':'http://api.songkick.com/api/3.0/artists/mbid:8e9516ba-f417-47dd-a8a5-8998b94553f8.json'}]}}], 'ageRestriction': None, 'flaggedAsEnded': False, 'venue': {'id': 2049, 'displayName': 'The Cabooze', 'uri': 'http://www.songkick.com/venues/2049-cabooze?utm_source=47812&utm_medium=partner', 'metroArea': {'displayName': 'Twin Cities', 'country': {'displayName': 'US'}, 'state': {'displayName': 'MN'}, 'id': 35130, 'uri': 'http://www.songkick.com/metro_areas/35130-us-twin-cities?utm_source=47812&utm_medium=partner'}, 'lat': 44.96341, 'lng': -93.2469}, 'location': {'city': 'Minneapolis, MN, US', 'lat': 44.96341, 'lng':
 -93.2469}}, {'id': 39028939, 'displayName': 'The Maine at Varsity Theater (November 16, 2019) (CANCELLED) ', 'type': 'Concert', 'uri': 'http://www.songkick.com/concerts/39028939-maine-at-varsity-theater?utm_source=47812&utm_medium=partner', 'status': 'cancelled', 'popularity': 0.060888, 'start': {'date': '2019-11-16', 'datetime': '2019-11-16T18:00:00-0600', 'time': '18:00:00'},
'performance': [{'id': 73918464, 'displayName': 'The Maine', 'billing': 'headline', 'billingIndex': 1, 'artist': {'id': 59712, 'displayName': 'The Maine', 'uri': 'http://www.songkick.com/artists/59712-maine?utm_source=47812&utm_medium=partner', 'identifier': [{'mbid': '7bd47e67-ecd5-49d5-837f-c692df38da4e', 'href': 'http://api.songkick.com/api/3.0/artists/mbid:7bd47e67-ecd5-49d5-837f-c692df38da4e.json'}]}}], 'ageRestriction': None, 'flaggedAsEnded': False, 'venue': {'id': 5546, 'displayName': 'Varsity Theater', 'uri': 'http://www.songkick.com/venues/5546-varsity-theater?utm_source=47812&utm_medium=partner', 'metroArea': {'displayName': 'Twin Cities', 'country': {'displayName': 'US'}, 'state': {'displayName': 'MN'}, 'id': 35130, 'uri': 'http://www.songkick.com/metro_areas/35130-us-twin-cities?utm_source=47812&utm_medium=partner'}, 'lat': 44.98081, 'lng': -93.23684}, 'location': {'city': 'Minneapolis, MN, US', 'lat': 44.98081, 'lng': -93.23684
}}, {'id': 38669939, 'displayName': 'The Okee Dokee Brothers at Ordway Center for the Performing Arts (November 17, 2019)', 'type': 'Concert', 'uri': 'http://www.songkick.com/concerts/38669939-okee-dokee-brothers-at-ordway-center-for-the-performing-arts?utm_source=47812&utm_medium=partner', 'status': 'ok', 'popularity': 0.00047, 'start': {'date': '2019-11-17', 'datetime': None, 'time': None}, 'performance': [{'id': 73298594, 'displayName': 'The Okee Dokee Brothers', 'billing': 'headline', 'billingIndex': 1, 'artist': {'id': 2749591, 'displayName': 'The Okee Dokee Brothers', 'uri': 'http://www.songkick.com/artists/2749591-okee-dokee-brothers?utm_source=47812&utm_medium=partner', 'identifier': [{'mbid': '9a402566-c57a-4ec5-85dd-2c52b588e6d8', 'href': 'http://api.songkick.com/api/3.0/artists/mbid:9a402566-c57a-4ec5-85dd-2c52b588e6d8.json'}]}}], 'ageRestriction': None, 'flaggedAsEnded': False, 'venue': {'id': 28712, 'displayName': 'Ordway Center for the Performing Arts', 'uri': 'http://www.songkick.com/venues/28712-ordway-center-for-the-performing-arts?utm_source=47812&utm_medium=partner', 'metroArea': {'displayName': 'Twin Cities', 'country': {'displayName': 'US'}, 'state': {'displayName': 'MN'}, 'id': 35130, 'uri': 'http://www.songkick.com/metro_areas/35130-us-twin-cities?utm_source=47812&utm_medium=partner'}, 'lat':
44.94458, 'lng': -93.09765}, 'location': {'city': 'St. Paul, MN, US', 'lat': 44.94458, 'lng': -93.09765}}, {'id': 39016861, 'displayName': 'Misterwives at Varsity Theater (November 17, 2019)', 'type': 'Concert' ,'uri':'http://www.songkick.com/concerts/39016861-misterwives-at-varsity-theater?utm_source=47812&utm_medium=partner', 'status':'ok', 'popularity': 0.056872, 'start': {'date': '2019-11-17', 'datetime': None, 'time': None}, 'performance': [{'id': 73898769, 'displayName': 'Misterwives', 'billing': 'headline', 'billingIndex': 1, 'artist': {'id': 6325384, 'displayName': 'Misterwives', 'uri': 'http://www.songkick.com/artists/6325384-misterwives?utm_source=47812&utm_medium=partner', 'identifier': [{'mbid': '5b6bac92-9b60-4e96-ac13-935bb6941b96', 'href': 'http://api.songkick.com/api/3.0/artists/mbid:5b6bac92-9b60-4e96-ac13-935bb6941b96.json'}]}}], 'ageRestriction': None, 'flaggedAsEnded': False, 'venue': {'id': 5546, 'displayName': 'Varsity Theater', 'uri': 'http://www.songkick.com/venues/5546-varsity-theater?utm_source=47812&utm_medium=partner', 'metroArea': {'displayName': 'Twin Cities', 'country': {'displayName': 'US'}, 'state': {'displayName': 'MN'}, 'id': 35130, 'uri': 'http://www.songkick.com/metro_areas/35130-us-twin-cities?utm_source=47812&utm_medium=partner'}, 'lat': 44.98081, 'lng': -93.23684}, 'location': {'city': 'Minneapolis, MN, US', 'lat': 44.98081, 'lng': -93.23684}}, {'id': 38904499, 'displayName': 'Briston Maroney at 7th St Entry (November 18, 2019)', 'type': 'Concert', 'uri': 'http://www.songkick.com/concerts/38904499-briston-maroney-at-7th-st-entry?utm_source=47812&utm_medium=partner', 'status': 'ok', 'popularity': 0.00105, 'start': {'date': '2019-11-18', 'datetime': '2019-11-18T19:00:00-0600', 'time': '19:00:00'}, 'performance': [{'id': 73704869, 'displayName': 'Briston Maroney', 'billing': 'headline', 'billingIndex': 1, 'artist': {'id': 9176989, 'displayName': 'Briston Maroney', 'uri': 'http://www.songkick.com/artists/9176989-briston-maroney?utm_source=47812&utm_medium=partner', 'identifier': [{'mbid': 'c0dea069-4f46-4f44-8f44-76831e6abb07',
 'href': 'http://api.songkick.com/api/3.0/artists/mbid:c0dea069-4f46-4f44-8f44-76831e6abb07.json'}]}}], 'ageRestriction': None, 'flaggedAsEnded': False, 'venue': {'id': 3720729, 'displayName'
: '7th St Entry', 'uri': 'http://www.songkick.com/venues/3720729-7th-st-entry?utm_source=47812&utm_medium=partner', 'metroArea': {'displayName': 'Twin Cities', 'country': {'displayName': 'US'
}, 'state': {'displayName': 'MN'}, 'id': 35130, 'uri': 'http://www.songkick.com/metro_areas/35130-us-twin-cities?utm_source=47812&utm_medium=partner'}, 'lat': 44.97827, 'lng': -93.27608}, 'location': {'city': 'Minneapolis, MN, US', 'lat': 44.97827, 'lng': -93.27608}}, {'id': 37822399, 'displayName': 'Jud Hailey at The Narrows Saloon (November 19, 2019)', 'type': 'Concert', 'uri':
 'http://www.songkick.com/concerts/37822399-jud-hailey-at-narrows-saloon?utm_source=47812&utm_medium=partner', 'status': 'ok', 'popularity': 0.0, 'start': {'date': '2019-11-19', 'datetime': '2019-11-19T19:00:00-0600', 'time': '19:00:00'}, 'performance': [{'id': 71835239, 'displayName': 'Jud Hailey', 'billing': 'headline', 'billingIndex': 1, 'artist': {'id': 9845004, 'displayName'
: 'Jud Hailey', 'uri': 'http://www.songkick.com/artists/9845004-jud-hailey?utm_source=47812&utm_medium=partner', 'identifier': []}}], 'ageRestriction': None, 'flaggedAsEnded': False, 'venue':
 {'id': 423691, 'displayName': 'The Narrows Saloon', 'uri': 'http://www.songkick.com/venues/423691-narrows-saloon?utm_source=47812&utm_medium=partner', 'metroArea': {'displayName': 'Twin Cities', 'country': {'displayName': 'US'}, 'state': {'displayName': 'MN'}, 'id': 35130, 'uri': 'http://www.songkick.com/metro_areas/35130-us-twin-cities?utm_source=47812&utm_medium=partner'}, 'lat': 44.93464, 'lng': -93.60893}, 'location': {'city': 'Navarre, MN, US', 'lat': 44.93464, 'lng': -93.60893}}, {'id': 38437069, 'displayName': 'Our Last Night at Fine Line (November 19, 2019)'
, 'type': 'Concert', 'uri': 'http://www.songkick.com/concerts/38437069-our-last-night-at-fine-line?utm_source=47812&utm_medium=partner', 'status': 'ok', 'popularity': 0.028019, 'start': {'date': '2019-11-19', 'datetime': '2019-11-19T18:00:00-0600', 'time': '18:00:00'}, 'performance': [{'id': 72900514, 'displayName': 'Our Last Night', 'billing': 'headline', 'billingIndex': 1, 'artist': {'id': 365740, 'displayName': 'Our Last Night', 'uri': 'http://www.songkick.com/artists/365740-our-last-night?utm_source=47812&utm_medium=partner', 'identifier': [{'mbid': '5466b02a-4465-4e87-b372-584cd5f97bff', 'href': 'http://api.songkick.com/api/3.0/artists/mbid:5466b02a-4465-4e87-b372-584cd5f97bff.json'}]}}], 'ageRestriction': None, 'flaggedAsEnded': False, 'venue': {'id': 1119, 'displayName': 'Fine Line', 'uri': 'http://www.songkick.com/venues/1119-fine-line?utm_source=47812&utm_medium=partner', 'metroArea': {'displayName': 'Twin Cities', 'country': {'displayName': 'US'}, 'state': {'displayName': 'MN'}, 'id': 35130, 'uri': 'http://www.songkick.com/metro_areas/35130-us-twin-cities?utm_source=47812&utm_medium=partner'}, 'lat': 44.98139, 'lng': -
93.27249}, 'location': {'city': 'Minneapolis, MN, US', 'lat': 44.98139, 'lng': -93.27249}}, {'id': 38950030, 'displayName': 'Son Little and Christopher Paul Stelling at Cedar Cultural Center(November 19, 2019)', 'type': 'Concert', 'uri': 'http://www.songkick.com/concerts/38950030-son-little-at-cedar-cultural-center?utm_source=47812&utm_medium=partner', 'status': 'ok', 'popularity': 0.012345, 'start': {'date': '2019-11-19', 'datetime': '2019-11-19T19:30:00-0600', 'time': '19:30:00'}, 'performance': [{'id': 73785249, 'displayName': 'Son Little', 'billing': 'headline',
 'billingIndex': 1, 'artist': {'id': 7884254, 'displayName': 'Son Little', 'uri': 'http://www.songkick.com/artists/7884254-son-little?utm_source=47812&utm_medium=partner', 'identifier': [{'mbid': '4bbcd67e-c6f5-43f3-ac66-9ffa8552d9f2', 'href': 'http://api.songkick.com/api/3.0/artists/mbid:4bbcd67e-c6f5-43f3-ac66-9ffa8552d9f2.json'}]}}, {'id': 73785250, 'displayName': 'Christopher Paul Stelling', 'billing': 'headline', 'billingIndex': 2, 'artist': {'id': 2929111, 'displayName': 'Christopher Paul Stelling', 'uri': 'http://www.songkick.com/artists/2929111-christopher-paul-stelling?utm_source=47812&utm_medium=partner', 'identifier': [{'mbid': '82ae7173-a51e-43d5-bd00-9316623041f1', 'href': 'http://api.songkick.com/api/3.0/artists/mbid:82ae7173-a51e-43d5-bd00-9316623041f1.json'}]}}], 'ageRestriction': None, 'flaggedAsEnded': False, 'venue': {'id': 5738, 'displayName': 'Cedar Cultural Center', 'uri': 'http://www.songkick.com/venues/5738-cedar-cultural-center?utm_source=47812&utm_medium=partner', 'metroArea': {'displayName': 'Twin Cities', 'country': {'displayName': 'US'}, 'state': {'displayName': 'MN'}, 'id': 35130, 'uri': 'http://www.songkick.com/metro_areas/35130-us-twin-cities?utm_source=47812&utm_medium=partner'}, 'lat': 44.96944, 'lng': -93.2476}, 'location': {'city': 'Minneapolis, MN, US', 'lat': 44.96944, 'lng': -93.2476}}]
    print(f'len(event_data) -> {len(event_data)}')
    print(f'event_data[0] -> {event_data[0]}')
    print(f'type(event_data[0] -> {type(event_data[0])}')
    for i in event_data:
        print(f'type -> {type(i)}')

    with multiprocessing.Pool(5) as pool:
        map_events = pool.map(build_event, [event for event in event_data])
        async_events = [pool.apply_async(build_event, [event for event in event_data])]
        imap_events = pool.imap(build_event_star, event_data)
        imap_unordered_events = pool.imap_unordered(build_event_star, event_data)

        # for x in map_events:
        #     r = x.result()
        #     print(f'type(r) -> {type(r)}')

        print('Ordered results using pool.apply_async():')
        for r in async_events:
            print('\t', r.get(timeout=1))
        print()

        print('Ordered results using pool.imap():')
        for x in imap_events:
            print('\t', x)
        print()

        print('Unordered results using pool.imap_unordered():')
        for y in imap_unordered_events:
            print('\t', y)
        print()

        print('Ordered results using pool.map() --- will block till complete:')
        for z in pool.map(build_event_star, event_data):
            print('\t', z)
        print()

if __name__ == '__main__':
    test_data = [
        {
            'id': 38830059,
            'displayName': 'Aaron Lewis at Mystic Lake Casino Hotel (November 16, 2019)',
            'type': 'Concert',
            'uri': 'http://www.songkick.com/concerts/38830059-aaron-lewis-at-mystic-lake-casino-hotel?utm_source=47812&utm_medium=partner',
            'status': 'ok',
            'popularity': 0.021507,
            'start': {'date': '2019-11-16','datetime': '2019-11-16T20:00:00-0600','time': '20:00:00'},
            'performance':
                [{'id': 73576549,'displayName': 'Aaron Lewis','billing': 'headline','billingIndex': 1,'artist': {'id': 89047,'displayName': 'Aaron Lewis','uri': 'http://www.songkick.com/artists/89047-aaron-lewis?utm_source=47812&utm_medium=partner','identifier': [{'mbid': 'c0d7ce5f-5602-4dec-a43b-ed3ee69a410f','href': 'http://api.songkick.com/api/3.0/artists/mbid:c0d7ce5f-5602-4dec-a43b-ed3ee69a410f.json'}, { 'mbid': '86034d1d-f66e-426d-ad52-ca5511a9b428','href': 'http://api.songkick.com/api/3.0/artists/mbid:86034d1d-f66e-426d-ad52-ca5511a9b428.json'}]}}],
            'ageRestriction': None,
            'flaggedAsEnded': False,
            'venue':
                {'id': 530,'displayName': 'Mystic Lake Casino Hotel','uri': 'http://www.songkick.com/venues/530-mystic-lake-casino-hotel?utm_source=47812&utm_medium=partner','metroArea': {'displayName': 'Twin Cities','country': {'displayName': 'US'},'state': {'displayName': 'MN'},'id': 35130,'uri': 'http://www.songkick.com/metro_areas/35130-us-twin-cities?utm_source=47812&utm_medium=partner'},'lat': 44.72963,'lng': -93.47499},
            'location': {'city': 'Prior Lake, MN, US','lat': 44.72963,'lng': -93.47499}
        },

        {
            'id': 38830059,
            'displayName': 'Aaron Lewis at Mystic Lake Casino Hotel (November 16, 2019)',
            'type': 'Concert',
            'uri': 'http://www.songkick.com/concerts/38830059-aaron-lewis-at-mystic-lake-casino-hotel?utm_source=47812&utm_medium=partner',
            'status': 'ok',
            'popularity': 0.021507,
            'start': {'date': '2019-11-16', 'datetime': '2019-11-16T20:00:00-0600', 'time': '20:00:00'},
            'performance':
                [{'id': 73576549, 'displayName': 'Aaron Lewis', 'billing': 'headline', 'billingIndex': 1,'artist': {'id': 89047, 'displayName': 'Aaron Lewis','uri': 'http://www.songkick.com/artists/89047-aaron-lewis?utm_source=47812&utm_medium=partner', 'identifier': [{'mbid': 'c0d7ce5f-5602-4dec-a43b-ed3ee69a410f','href': 'http://api.songkick.com/api/3.0/artists/mbid:c0d7ce5f-5602-4dec-a43b-ed3ee69a410f.json'},{'mbid': '86034d1d-f66e-426d-ad52-ca5511a9b428','href': 'http://api.songkick.com/api/3.0/artists/mbid:86034d1d-f66e-426d-ad52-ca5511a9b428.json'}]}}],
            'ageRestriction': None,
            'flaggedAsEnded': False,
            'venue':
                {'id': 530, 'displayName': 'Mystic Lake Casino Hotel','uri': 'http://www.songkick.com/venues/530-mystic-lake-casino-hotel?utm_source=47812&utm_medium=partner','metroArea': {'displayName': 'Twin Cities', 'country': {'displayName': 'US'}, 'state': {'displayName': 'MN'}, 'id': 35130, 'uri': 'http://www.songkick.com/metro_areas/35130-us-twin-cities?utm_source=47812&utm_medium=partner'}, 'lat': 44.72963,'lng': -93.47499},
            'location': {'city': 'Prior Lake, MN, US', 'lat': 44.72963, 'lng': -93.47499}
        }
    ]


    sk_events_list = parallel_get_events(test_data)
    for ske in sk_events_list:
        print(f'type(event) -> {type(ske)}')
        print(ske)

    # pool = multiprocessing.Pool(processes=5)
    # result = pool.apply_async(build_event, test_data)
    # print(result.get(timeout=1))
    # print(pool.map(build_event, test_data))
    #
    # it = pool.imap(build_event, test_data)
    # print(next(it))

    # test()
    # with Pool(5) as p:
    #     p = Process(target=build_event,args=)





