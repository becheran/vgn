import pytest
import asyncio
from vgn.functions import *

test_loop = asyncio.get_event_loop()


@pytest.mark.asyncio
async def test_api_version_did_not_change():
    async with VGNClient() as vgn_client:
        assert (await vgn_client.api_version()) == 'Puls-API-v1.2'


@pytest.mark.asyncio
async def test_find_stations():
    async with VGNClient() as vgn_client:
        s = await vgn_client.stations("Rennweg")
        assert len(s) > 0


@pytest.mark.asyncio
async def test_find_not_a_station():
    async with VGNClient() as vgn_client:
        assert len(await vgn_client.stations("This_is_Not_a_station")) == 0


@pytest.mark.asyncio
async def test_no_nearby_locations():
    async with VGNClient() as vgn_client:
        assert len(await vgn_client.nearby_stations(Coordinates(1, 1))) == 0


@pytest.mark.asyncio
async def test_nearby_locations():
    async with VGNClient() as vgn_client:
        near_plaerrer = await vgn_client.nearby_stations(
            Coordinates(latitude=49.4480881582118, longitude=11.0647882822154), 5)
        assert len(near_plaerrer) == 1
        assert near_plaerrer[0].name == 'Plärrer (Nürnberg)'


@pytest.mark.asyncio
async def test_depatures():
    async with VGNClient() as vgn_client:
        dep_plaerrer = await vgn_client.departure_schedule(704)
        assert len(dep_plaerrer) > 0


@pytest.mark.asyncio
async def test_depatures_for_line():
    async with VGNClient() as vgn_client:
        dep_plaerrer = await vgn_client.departure_schedule_for_line(704, 'U2')
    assert len(dep_plaerrer) > 0
