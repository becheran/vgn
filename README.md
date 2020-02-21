# VGN

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Version](https://img.shields.io/pypi/v/vgn)
[![PyPI download month](https://img.shields.io/pypi/dm/vgn.svg)](https://pypi.python.org/pypi/vgn/)
[![Python versions](https://img.shields.io/pypi/pyversions/vgn.svg)](https://img.shields.io/pypi/pyversions/vgn)
[![Documentation Status](https://readthedocs.org/projects/vgn/badge/?version=stable)](https://vgn.readthedocs.io/en/stable/?badge=stable)
[![Build Status](https://gitlab.com/becheran/vgn_ci_job/badges/master/pipeline.svg)](https://gitlab.com/becheran/vgn_ci_job/pipelines)

Asynchron Python API for the *Verkehrsverbund Grossraum Nuernberg (VGN)*.

Uses the official [REST-API](https://start.vag.de/dm/) to query realtime public transport information for Nuremberg.

With the python 3.7 feature [asyncio tasks](https://docs.python.org/3/library/asyncio-task.html) fast and non-blocking querries are possible.

[Read the docs](https://vgn.readthedocs.io/en/stable/) for more information.

Consider installing `cchardet` and  `aiodns` via pip for speedup (see the [aiohttp documentation](https://docs.aiohttp.org/en/stable/)).

## Example

``` python
import vgn
import asyncio


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
```
