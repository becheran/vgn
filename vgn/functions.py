from vgn.exceptions import VgnGetError
from vgn.data_classes import *
import vgn.converter as conv
import datetime
import asyncio
import aiohttp


class VGNClient:
    async def __aenter__(self):
        self._client_session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._client_session.__aexit__(*args, **kwargs)

    @staticmethod
    def _url(path):
        return 'https://start.vag.de/dm/api/v1/' + path

    async def _get(self, query) -> dict:
        async with self._client_session.get(query) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                raise VgnGetError(f'Could not resolve query {query}. Returned {resp.status}')

    async def api_version(self) -> str:
        """ Version info from the VGN REST-API."""
        query = self._url('haltestellen/VGN/location?lon=0&lat=0')
        return (await self._get(query)).get('Metadata').get('Version')

    async def all_stations(self) -> List[Station]:
        """ List of all stations.

        Returns:
            list: List of stations for the VGN transport association.
        """
        query = self._url(f'haltestellen/VGN')
        return conv.to_stations((await self._get(query)).get('Haltestellen'))

    async def stations(self, station_name: str) -> List[Station]:
        """ List of stations for the specified station name.

        Args:
            station_name: Name of a station.
        Returns:
            list: List of station objects for the given stop_name.
        """
        query = self._url(f'haltestellen/VGN?name={station_name}') if station_name else _url(f'haltestellen/VGN')
        return conv.to_stations((await self._get(query)).get('Haltestellen'))

    async def nearby_stations(self, location: Coordinates, radius: int = 1000) -> List[Station]:
        """ List stops close to a given location.

        Args:
            location: Search for stations close to this location.
            radius (optional): Radius for search in meter

        Returns:
            list: List of station objects in radius of the given location.
        """
        query = self._url(f'haltestellen/VGN/location?lon={location.longitude}&lat={location.latitude}&radius={radius}')
        return conv.to_stations((await self._get(query)).get('Haltestellen'))

    async def station_additional_information(self, stop_id: int) -> List[str]:
        """ List of information text strings for a given stop.

        Args:
            stop_id (optional): The VGN stop identifier number.

        Returns:
            list: List of strings containing additional information for the given station.
        """
        query = self._url(f'abfahrten/VGN/{stop_id}')
        return (await self._get(query)).get('Sonderinformationen')

    async def departure_schedule(self,
                                 stop_id: int,
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
        query = self._url(
            f'abfahrten/VGN/{stop_id}'
            f'?product={transport_type_str}'
            f'&timespan={timespan}'
            f'&timedelay={timedelay}'
            f'&limitcount={limit_result}')
        return conv.to_departures((await self._get(query)).get('Abfahrten'))

    async def departure_schedule_for_line(self,
                                          stop_id: int,
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
        query = self._url(f'abfahrten/VGN/{stop_id}/{line_name}'
                          f'?timespan={timespan}'
                          f'&timedelay={timedelay}'
                          f'&limitcount={limit_result}')
        return conv.to_departures((await self._get(query)).get('Abfahrten'))

    async def rides(self, transport_type: TransportType, time_span: int = 60) -> List[Ride]:
        """ All running and starting rides for a given transport type within a given time frame (default 60 minutes)

        Args:
            transport_type: Transportation type. For example Bus.
            time_span (optional): Time window in minutes (default 60 minutes)

        Returns:
            list: List of rides for the given transport type within the time window.
        """
        query = self._url(f'fahrten/{transport_type.value}?timespan={time_span}')
        return conv.to_rides((await self._get(query)).get('Fahrten'))

    async def route(self, transport_type: TransportType, ride_id: int) -> Route:
        """ Route for a given transport type and ride number for the current operating day

        Args:
            transport_type: Transportation type. For example Bus.
            ride_id: Ride number for the given transportation type

        Returns:
            Route: The route for the given ride_number
        """
        query = self._url(f'fahrten/{transport_type.value}/{ride_id}')
        return conv.to_route((await self._get(query)))

    async def route_for_day(self, transport_type: TransportType, ride_id: int, day: datetime.date) -> Route:
        """ Route for a given transport type, ride number and operating day.

        Args:
            transport_type: Transportation type. For example Bus.
            ride_id: Ride number for the given transportation type.
            day: Operating day date for the request.

        Returns:
            Route: The route for the given ride_number on the requested day.
        """
        query = self._url(f'fahrten/{transport_type.value}/{day}/{ride_id}')
        return conv.to_route((await self._get(query)))


async def main():
    async with VGNClient() as vgn_client:
        res = await asyncio.gather(
            vgn_client.api_version(),
            vgn_client.all_stations(),
            vgn_client.departure_schedule(704),
            vgn_client.departure_schedule_for_line(704, "U2"),
            vgn_client.rides(TransportType.BUS, 30),
        )
    print(f'Api version: {res[0]}')
    print(f'Stations in nbg: {str(len(res[1]))}')
    print(f'Departures at plaerrer in nbg: {res[2]}')
    print(f'Departures of underground line 2 at plaerrer in nbg: {res[3]}')
    print(f'Bus departures in the next 30 minutes: {res[4]}')


if __name__ == '__main__':
    asyncio.run(main())
