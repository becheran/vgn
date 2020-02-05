from vgn.functions import *


def test_api_version_did_not_change():
    assert api_version() == 'Puls-API-v1.2'


def test_find_stations():
    assert len(stations("Rennweg")) > 0


def test_find_not_a_station():
    assert len(stations("This_is_Not_a_station")) == 0


def test_no_nearby_locations():
    assert len(nearby_stations(Coordinates(1, 1))) == 0


def test_nearby_locations():
    near_plaerrer = nearby_stations(Coordinates(latitude=49.4480881582118, longitude=11.0647882822154), 5)
    assert len(near_plaerrer) == 1
    assert near_plaerrer[0].name == 'Plärrer (Nürnberg)'


def test_depatures():
    dep_plaerrer = departure_schedule(704)
    assert len(dep_plaerrer) > 0


def test_depatures_for_line():
    dep_plaerrer = departure_schedule_for_line(704, 'U2')
    assert len(dep_plaerrer) > 0


def test_route_for_day():
    rou_day = route_for_day(TransportType.BUS, 2008502, datetime.date(2020, 2, 6))
    assert rou_day.transport_type == TransportType.BUS
