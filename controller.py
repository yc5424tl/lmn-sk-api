import logging
from sk_factory import Factory

log = logging.getLogger()
factory = Factory()

def instance_call(data_dict: dict, call: str):
    if not data_dict:
        return []
    else:
        switcher = {
            'artist':      factory.build_artist,
            'city':        factory.build_city,
            'event':       factory.build_event,
            'location':    factory.build_location,
            'venue':       factory.build_venue,
            'metro_area':  factory.build_metro_area,
            'performance': factory.build_performances}
        function_call = switcher.get(call)
        return function_call(data_dict)


def instantiate_list_data(list_data: [{}], call: str):
    if not list_data:
        return []
    else:
        instance_list = []
        for data in list_data:
            try:
                new_instance = instance_call(data_dict=data, call=call)
                instance_list.append(new_instance)
            except KeyError as kE:
                log.log(msg=f'KeyError {kE} during {call} instance call passing {data}', level=Warning)
            except TypeError as tE:
                log.log(msg=f'TypeError {tE} during {call} instance call passing {data}', level=Warning)
                continue
        return instance_list