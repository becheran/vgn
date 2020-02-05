# VGN

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Version](https://img.shields.io/pypi/v/vgn)
[![PyPI download month](https://img.shields.io/pypi/dm/vgn.svg)](https://pypi.python.org/pypi/vgn/)
[![Python versions](https://img.shields.io/pypi/pyversions/vgn.svg)](https://img.shields.io/pypi/pyversions/vgn)
[![Documentation Status](https://readthedocs.org/projects/vgn/badge/?version=latest)](https://vgn.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://gitlab.com/becheran/vgn_ci_job/badges/master/pipeline.svg)](https://gitlab.com/becheran/vgn_ci_job/pipelines)

Python API for the *Verkehrsverbund Grossraum Nuernberg (VGN)*.

Uses the official [REST-API](https://start.vag.de/dm/) to query realtime public transport information for Nuremberg.

[Read the docs](https://vgn.readthedocs.io/en/latest/) for more information.

## Example

``` python
import vgn

# Print all departures for the station with ID 704 (Nuernberg Plaerrer)
print(vgn.departure_schedule(704))
# Print all departures of the underground line two for the Nuernberg Plaerrer station
print(vgn.departure_schedule_for_line(704, "U2"))
# Get all bus rides in the VGN network within the timeframe of 30 minutes
print(vgn.rides(vgn.TransportType.BUS, 30))
# Return the route of bus with the ride id 2008502 for the current day
```
