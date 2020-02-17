import requests
from vgn.exceptions import VgnGetError
from vgn.data_classes import *
import vgn.converter as conv
import datetime


def _url(path):
    return 'https://start.vag.de/dm/api/v1/' + path


def _get(query) -> dict:
    resp = requests.get(query)
    if resp.status_code == 200:
        return resp.json()
    else:
        raise VgnGetError(f'Could not resolve query {query}. Returned {resp.status_code}')


def api_version() -> str:
    """ Version info from the VGN REST-API."""
    query = _url('haltestellen/VGN/location?lon=0&lat=0')
    return _get(query).get('Metadata').get('Version')


def all_stations() -> List[Station]:
    """ List of all stations.

    Returns:
        list: List of stations for the VGN transport association.
    """
    query = _url(f'haltestellen/VGN')
    return conv.to_stations(_get(query).get('Haltestellen'))


def stations(station_name: str) -> List[Station]:
    """ List of stations for the specified station name.

    Args:
        station_name: Name of a station.
    Returns:
        list: List of station objects for the given stop_name.
    """
    query = _url(f'haltestellen/VGN?name={station_name}') if station_name else _url(f'haltestellen/VGN')
    return conv.to_stations(_get(query).get('Haltestellen'))


def nearby_stations(location: Coordinates, radius: int = 1000) -> List[Station]:
    """ List stops close to a given location.

    Args:
        location: Search for stations close to this location.
        radius (optional): Radius for search in meter

    Returns:
        list: List of station objects in radius of the given location.
    """
    query = _url(f'haltestellen/VGN/location?lon={location.longitude}&lat={location.latitude}&radius={radius}')
    return conv.to_stations(_get(query).get('Haltestellen'))


def station_additional_information(stop_id: int) -> List[str]:
    """ List of information text strings for a given stop.

    Args:
        stop_id (optional): The VGN stop identifier number.

    Returns:
        list: List of strings containing additional information for the given station.
    """
    query = _url(f'abfahrten/VGN/{stop_id}')
    return _get(query).get('Sonderinformationen')


def departure_schedule(stop_id: int,
                       transport_type: List[TransportType] = [TransportType.BUS, TransportType.TRAM,
                                                              TransportType.SUBWAY],
                       timespan: int = 10,
                       timedelay: int = 5,
                       limit_result: int = 100) -> List[Departure]:
    """ Departures for a specific stop.

    Args:
        stop_id: The VGN stop identifier number.
        transport_type: Information shall only be given for the defined transport means of transportation.
        limit_result (optional): Limit amount of returned results. Default limit is 100.
        timedelay (optional): Time delay for the request in minutes.
        timespan (optional): Time window for the query in minutes.

    Returns:
        list: List of departures for the given station.
    """
    if limit_result <= 0:
        limit_result = 100
    transport_type_str = ','.join(list(map(lambda x: x.value, transport_type)))
    query = _url(
        f'abfahrten/VGN/{stop_id}'
        f'?product={transport_type_str}'
        f'&timespan={timespan}'
        f'&timedelay={timedelay}'
        f'&limitcount={limit_result}')
    return conv.to_departures(_get(query).get('Abfahrten'))


def departure_schedule_for_line(stop_id: int,
                                line_name: str,
                                timespan: int = 10,
                                timedelay: int = 5,
                                limit_result: int = 100) -> List[Departure]:
    """ List of  Departures for a specific stop and line.

    Args:
        line_name: Name of the line. For example 'U2' for the underground line two.
        stop_id: The VGN stop identifier number.
        limit_result (optional): Limit amount of returned results. Default limit is 100.
        timedelay (optional): Time delay for the request in minutes.
        timespan (optional): Time window for the query in minutes.

    Returns:
        list: List of departures for the given station and line.
    """
    if limit_result <= 0:
        limit_result = 100
    query = _url(f'abfahrten/VGN/{stop_id}/{line_name}'
                 f'?timespan={timespan}'
                 f'&timedelay={timedelay}'
                 f'&limitcount={limit_result}')
    return conv.to_departures(_get(query).get('Abfahrten'))


def rides(transport_type: TransportType, time_span: int = 60) -> List[Ride]:
    """ All running and starting rides for a given transport type within a given time frame (default 60 minutes)

    Args:
        transport_type: Transportation type. For example Bus.
        time_span (optional): Time window in minutes (default 60 minutes)

    Returns:
        list: List of rides for the given transport type within the time window.
    """
    query = _url(f'fahrten/{transport_type.value}?timespan={time_span}')
    return conv.to_rides(_get(query).get('Fahrten'))


def route(transport_type: TransportType, ride_id: int) -> Route:
    """ Route for a given transport type and ride number for the current operating day

    Args:
        transport_type: Transportation type. For example Bus.
        ride_id: Ride number for the given transportation type

    Returns:
        Route: The route for the given ride_number
    """
    query = _url(f'fahrten/{transport_type.value}/{ride_id}')
    return conv.to_route(_get(query))


def route_for_day(transport_type: TransportType, ride_id: int, day: datetime.date) -> Route:
    """ Route for a given transport type, ride number and operating day.

    Args:
        transport_type: Transportation type. For example Bus.
        ride_id: Ride number for the given transportation type.
        day: Operating day date for the request.

    Returns:
        Route: The route for the given ride_number on the requested day.
    """
    query = _url(f'fahrten/{transport_type.value}/{day}/{ride_id}')
    return conv.to_route(_get(query))


if __name__ == '__main__':
    all_s = all_stations()
    print('Stations in nbg: ' + str(len(all_s)))
    print(all_s)
    dep = departure_schedule(704)
    dep_for_line = departure_schedule_for_line(704, "U2")
    rid = rides(TransportType.BUS, 30)
    # rou = route(TransportType.BUS, 2008502)
    # rou_day = route_for_day(TransportType.BUS, 2008502, datetime.date(2020, 2, 6))
    print(dep)
    print(dep_for_line)
    print(rid)
    # print(rou)
    # print(rou_day)
