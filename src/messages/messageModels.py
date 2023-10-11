#importing model from uagents module
from uagents import Model


# The message to server model, ie, the structur of the message sent by user to the server.
class MessageToServer(Model):
    city: str
    state: str
    country: str
    min_temp: float
    max_temp: float
    geoLocation: object

#  The monitor response model, ie, structure of the message sent by the server back to the user
class MonitorResponse(Model):
    current_temp: float
    out_of_range: bool



