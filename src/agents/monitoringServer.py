from uagents import Agent, Context, Model
from uagents.contrib.protocols.protocol_query import proto_query
from uagents.setup import fund_agent_if_low
import requests
import json
import os
from dotenv import load_dotenv
from plyer import notification
load_dotenv()

from messages.messageModels import MonitorResponse, MessageToServer
# from protocols.models import query_proto, LiveCurrencyModel


WeatherMonitor = Agent(
    name= "WeatherMonitor",
    port= 8001,
    seed="Weather monitor",
    endpoint={
        "http://127.0.0.1:8001/monitor": {},
    }
)
fund_agent_if_low(WeatherMonitor.wallet.address())

class TemperatureMonitoring:
    @staticmethod
    def fetch_live_temp(coordinates):
        latitude = coordinates["latitude"]
        longitude = coordinates["longitude"]
        
        OPENWEATHERAPI_KEY=os.getenv("OPENWEATHERAPI_KEY")
        OPENWEATHERAPI_URL=f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={OPENWEATHERAPI_KEY}"

        temperatures_live = requests.get(OPENWEATHERAPI_URL)
        if temperatures_live.status_code == 200:
            data = temperatures_live.json()
            temperature = data['main']['temp'] - 273.15
            print(temperature)
            return temperature
        else:
            print("Temperature fetch failed, this is most probably an API error")



@WeatherMonitor.on_event("startup")
async def startup_weather_agent(ctx: Context):
    os.putenv("SERVER_ADDRESS", ctx.address)

    ctx.logger.info(f"Weather Monitor up and running. The registered name is {ctx.name}, the address {ctx.address}")



@WeatherMonitor.on_message(model=MessageToServer)
async def server_message_handler(ctx: Context, sender: str, msg: MessageToServer):
    ctx.logger.info(f"Recieved message from {sender}: Location: {msg.city}, {msg.state}, {msg.country}, min_temp: {msg.min_temp}, max_temp: {msg.max_temp}, coordinates: {msg.geoLocation}") 
    
    live_temperature = TemperatureMonitoring.fetch_live_temp(msg.geoLocation)
    minimum = msg.min_temp
    maximum = msg.max_temp
    
    if live_temperature < minimum:
        user_alert = f"Temperature out of range!"
        notification.notify(
            title = 'Alert',
            message = f"Live temperature ({live_temperature}°C) is below minimum provided temperature!",
            app_icon = '',
            timeout = 3,
        )
    elif live_temperature > maximum:
        user_alert = f"Temperature out of range!"
        notification.notify(
            title = 'Alert',
            message = f"Live temperature ({live_temperature}°C) is above the maximum provided temperature!",
            app_icon = '',
            timeout = 3,
        )
    else:
        user_alert = f"Live temperature inside the given range."


    server_response = MonitorResponse(
        current_temp = live_temperature,
        out_of_range=(live_temperature < minimum or live_temperature > maximum)
    )
    
    await ctx.send(sender, server_response)

if __name__ == "__main__":
    WeatherMonitor.run()


