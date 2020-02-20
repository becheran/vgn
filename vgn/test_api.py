import pytest
from vgn.functions import *


@pytest.mark.asyncio
async def test_api_version_did_not_change():
    assert (await api_version()) == 'Puls-API-v1.2'


@pytest.mark.asyncio
async def test_find_stations():
    s = await stations("Rennweg")
    assert len(s) > 0


@pytest.mark.asyncio
async def test_find_not_a_station():
    assert len(await stations("This_is_Not_a_station")) == 0


@pytest.mark.asyncio
async def test_no_nearby_locations():
    assert len(await nearby_stations(Coordinates(1, 1))) == 0


@pytest.mark.asyncio
async def test_nearby_locations():
    near_plaerrer = await nearby_stations(Coordinates(latitude=49.4480881582118, longitude=11.0647882822154), 5)
    assert len(near_plaerrer) == 1
    assert near_plaerrer[0].name == 'Plärrer (Nürnberg)'


@pytest.mark.asyncio
async def test_depatures():
    dep_plaerrer = await departure_schedule(704)
    assert len(dep_plaerrer) > 0


@pytest.mark.asyncio
async def test_depatures_for_line():
    dep_plaerrer = await departure_schedule_for_line(704, 'U2')
    assert len(dep_plaerrer) > 0
