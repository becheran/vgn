import asyncio
from vgn.functions import *

test_loop = asyncio.get_event_loop()


def test_api_version_did_not_change():
    assert test_loop.run_until_complete(api_version()) == 'Puls-API-v1.2'


def test_find_stations():
    assert len(test_loop.run_until_complete(stations("Rennweg"))) > 0


def test_find_not_a_station():
    assert len(test_loop.run_until_complete(stations("This_is_Not_a_station"))) == 0


def test_no_nearby_locations():
    assert len(test_loop.run_until_complete(nearby_stations(Coordinates(1, 1)))) == 0


def test_nearby_locations():
    near_plaerrer = test_loop.run_until_complete(
        nearby_stations(Coordinates(latitude=49.4480881582118, longitude=11.0647882822154), 5))
    assert len(near_plaerrer) == 1
    assert near_plaerrer[0].name == 'Plärrer (Nürnberg)'


def test_depatures():
    dep_plaerrer = test_loop.run_until_complete(departure_schedule(704))
    assert len(dep_plaerrer) > 0


def test_depatures_for_line():
    dep_plaerrer = test_loop.run_until_complete(departure_schedule_for_line(704, 'U2'))
    assert len(dep_plaerrer) > 0
