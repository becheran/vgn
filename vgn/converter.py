from vgn.data_classes import *


def _to_datetime(iso_8601_str: str):
    if iso_8601_str:
        return datetime.datetime.strptime(iso_8601_str, "%Y-%m-%dT%H:%M:%S%z")
    else:
        return None


def _to_date(iso_8601_str: str):
    if iso_8601_str:
        return datetime.datetime.strptime(iso_8601_str, "%Y-%m-%d").date()
    else:
        return None


def _to_transport_type(type_string: str) -> TransportType:
    if type_string == 'Bus':
        return TransportType.BUS
    elif type_string == 'Tram':
        return TransportType.TRAM
    elif type_string == 'UBahn':
        return TransportType.SUBWAY
    else:
        raise TypeError(f'Unknown transport type {type_string}.')


def to_stations(returned_dict: dict) -> List[Station]:
    return list(map(lambda x: Station(x.get('Haltestellenname'),
                                      x.get('VGNKennung'),
                                      Coordinates(x.get('Latitude'), x.get('Longitude')),
                                      list(map(lambda z: _to_transport_type(z), x.get('Produkte').split(',')))
                                      ), returned_dict))


def to_departures(returned_dict: dict) -> List[Departure]:
    return list(map(lambda x: Departure(x.get('Linienname'),
                                        x.get('Haltepunkt'),
                                        x.get('Richtung'),
                                        x.get('Richtungstext'),
                                        _to_datetime(x.get('AbfahrtszeitSoll')),
                                        _to_datetime(x.get('AbfahrtszeitIst')),
                                        _to_transport_type(x.get('Produkt')),
                                        Coordinates(x.get('Latitude'), x.get('Longitude')),
                                        x.get('Fahrtnummer'),
                                        x.get('Fahrtartnummer'),
                                        x.get('Fahrzeugnummer'),
                                        x.get('Prognose')), returned_dict))


def to_rides(returned_dict: dict) -> List[Ride]:
    return list(map(lambda x: Ride(x.get('Fahrtnummer'),
                                   x.get('Linienname'),
                                   x.get('Richtung'),
                                   _to_date(x.get('Betriebstag')),
                                   _to_datetime(x.get('Startzeit')),
                                   _to_datetime(x.get('Endzeit')),
                                   x.get('StartHaltID'),
                                   x.get('EndHaltID'),
                                   x.get('Fahrzeugnummer')), returned_dict))


def to_route(returned_dict: dict) -> Route:
    line_name = returned_dict.get("Linienname")
    direction = returned_dict.get("Richtung")
    direction_text = returned_dict.get("Richtungstext")
    ride_id = returned_dict.get("Fahrtnummer")
    operating_day = _to_date(returned_dict.get("Betriebstag"))
    product = _to_transport_type(returned_dict.get('Produkt'))
    is_cancelled = bool(returned_dict.get("FaelltAus"))
    additional_ride = bool(returned_dict.get("Zusatzfahrt"))
    vehicle_number = returned_dict.get("Fahrzeugnummer")
    current_route = list(map(lambda x:
                             RoutePoint(x.get("Haltestellenname"),
                                        x.get("VGNKennung"),
                                        x.get("Haltepunkt"),
                                        _to_datetime(x.get("AnkunftszeitSoll")),
                                        _to_datetime(x.get("AnkunftszeitIst")),
                                        _to_datetime(x.get("AbfahrtszeitSoll")),
                                        _to_datetime(x.get("AbfahrtszeitIst")),
                                        x.get("Richtungstext"),
                                        Coordinates(x.get('Latitude'), x.get('Longitude')),
                                        False if x.get("Durchfahrt") is None else bool(x.get("Durchfahrt")),
                                        False if x.get("Einsteigeverbot") is None else bool(
                                            x.get("Einsteigeverbot")),
                                        False if x.get("Aussteigeverbot") is None else bool(
                                            x.get("Aussteigeverbot")),
                                        False if x.get("Zusatzhalt") is None else bool(x.get("Zusatzhalt")))
                             , returned_dict.get("Fahrtverlauf")))
    return Route(line_name, direction, direction_text, ride_id, operating_day, is_cancelled, additional_ride,
                 vehicle_number, product, current_route)
