from typing import List

from uagents import Context, Model, Protocol

class MessageToServer(Model):
    city: str
    state: str
    country: str
    min_temp: float
    max_temp: float
    geoLocation: object

class MonitorResponse(Model):
    current_temp: float
    out_of_range: bool



