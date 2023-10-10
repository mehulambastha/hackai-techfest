from uagents import Agent, Context, Model
import os
from messages.messageModels import MessageToServer, MonitorResponse
import requests
import json

User = Agent(
    name= "User agent",
    port= 8002,
    seed="User inputs",
    endpoint={
        "http://127.0.0.1:8002/user": {},
    }
)

user_data = {}
user_data["coordinates"] = {}

class InfoGeoLocation:
    @staticmethod
    def extract_latLong():

        api_url = 'https://api.api-ninjas.com/v1/geocoding?city={}&country={}'.format(user_data["city"], user_data["country"])
        response = requests.get(api_url, headers={'X-Api-Key': 'VP3uCGC3p15dWETZKt4XJg==oo0F9PM68aAtR866'})

        if response.status_code == requests.codes.ok: 
            json_formatted_response = json.loads(response.text)
            for location in json_formatted_response:
                if (location.get("country").lower() == user_data["country"] and location.get("state").lower() == user_data["state"] and location.get("name").lower() == user_data["city"]):
                    user_data["coordinates"]["latitude"] = location.get("latitude")
                    user_data["coordinates"]["longitude"] = location.get("longitude")
                    break
            
            if user_data["coordinates"]['latitude'] is not None and user_data["coordinates"]['longitude'] is not None:
                    return user_data["coordinates"]
            else:
                return None, None
                print("Coordinates for given location not found")  

        else:
            print("Error:", response.status_code, response.text)            

SERVER_ADDRESS=""
with open(".env", "r") as f:
    for line in f.readlines():
        try:
            key, value = line.split('=')
            os.putenv(key, value)
            SERVER_ADDRESS=value
        except ValueError:
            # syntax error
            pass

@User.on_event("startup")
async def startup_user_agent(ctx: Context):
    # fetching server address from .env file

    ctx.logger.info(f"User agent is running succesfully.\n\tAddress: {ctx.address}\n\tName: {ctx.name}")
    user_data["city"] = input("Enter city: ").lower()
    user_data["state"] = input("Enter state: ").lower()
    user_data["country"] = input("Enter country: ").lower()
    user_data["min_temp"] = float(input("Enter minimum temperature: "))
    user_data["max_temp"] = float(input("Enter maximum temperature: "))


# interval send
@User.on_interval(period=5)
async def send_data_to_server(ctx: Context):
    geoLocation = InfoGeoLocation.extract_latLong()
    await ctx.send(SERVER_ADDRESS, MessageToServer(city=user_data["city"], state=user_data["state"], country=user_data["country"], min_temp=user_data["min_temp"], max_temp=user_data["max_temp"], geoLocation=user_data["coordinates"]))

@User.on_message(model=MonitorResponse)
async def weather_monitor_response(ctx: Context, sender: str, msg: MonitorResponse):
    ctx.logger.info(f"Response from server address {sender}:\n Current Temp: {msg.current_temp}\nOut of range? {msg.out_of_range}")