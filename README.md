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

[Read the docs](https://vgn.readthedocs.io/en/latest/) for more information.

## Example

``` python
import vgn


async def main():
    res = await asyncio.gather(
        api_version(),
        all_stations(),
        departure_schedule(704),
        departure_schedule_for_line(704, "U2"),
        rides(TransportType.BUS, 30),
    )
    print(f'Api version: {res[0]}')
    print(f'Stations in nbg: {str(len(res[1]))}')
    print(f'Departures at plaerrer in nbg: {res[2]}')
    print(f'Departures of underground line 2 at plaerrer in nbg: {res[3]}')
    print(f'Bug departures in the next 30 minutes: {res[4]}')


if __name__ == '__main__':
    asyncio.run(main())
```
