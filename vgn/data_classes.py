from dataclasses import dataclass
from enum import Enum
from typing import List
import datetime


@dataclass()
class Coordinates:
    """ Coordinates in WGS 84 Format in degrees."""
    latitude: float
    longitude: float


@dataclass()
class TransportType(Enum):
    """ Type of transportation (e.g.: bus, tram, subway)."""
    BUS = 'Bus'
    TRAM = 'Tram'
    SUBWAY = 'UBahn'


@dataclass()
class Station:
    """ Station data object class."""
    name: str
    station_id: int
    coordinates: Coordinates
    transport_types: List[TransportType]


@dataclass()
class Departure:
    """ Departure data object class."""
    line_name: str
    station_id: str
    direction: str
    direction_text: str
    planned_departure_time: datetime.datetime
    actual_departure_time: datetime.datetime
    transport_type: TransportType
    coordinates: Coordinates
    ride_id: int
    ride_type_id: int
    vehicle_number: str
    forecast: bool


@dataclass()
class Ride:
    """ Ride data object class."""
    ride_id: int
    line_name: str
    direction: str
    operating_day: datetime.date
    start_time: datetime.datetime
    end_time: datetime.datetime
    start_station_id: str
    end_station_id: str
    vehicle_number: str


@dataclass()
class RoutePoint:
    """ Single stop of a route."""
    station_name: str
    station_id: int
    stop_point: str
    planned_arrival_time: datetime.datetime
    actual_arrival_time: datetime.datetime
    planned_departure_time: datetime.datetime
    actual_departure_time: datetime.datetime
    direction_text: str
    coordinates: Coordinates
    transit: bool
    no_boarding: bool
    no_get_off: bool
    additional_stop: bool


@dataclass()
class Route:
    """ Route for a specific ride."""
    line_name: str
    direction: str
    direction_text: str
    ride_id: int
    operating_day: datetime.date
    is_cancelled: bool
    additional_ride: bool
    vehicle_number: str
    transport_type: TransportType
    route: List[RoutePoint]
