from uagents import Agent, Context, Model
from uagents.contrib.protocols.protocol_query import proto_query
from uagents.setup import fund_agent_if_low
import requests
import os
from dotenv import load_dotenv
from plyer import notification
load_dotenv()

# importing the data models form messages folder and messageModels module
from messages.messageModels import MonitorResponse, MessageToServer

# Set up the WeatherMonitor Agent (the server)
WeatherMonitor = Agent(
    name= "WeatherMonitor",
    port= 8001,
    seed="Weather monitor",
    endpoint={
        "http://127.0.0.1:8001/monitor": {},
    }
)
# register the agent on the almanac
fund_agent_if_low(WeatherMonitor.wallet.address())

# Setup a temperature monitoring class to deal with everyhting related to fetching and manipulation of live temperatures
class TemperatureMonitoring:
    '''
        Function: fetch_live_temp
        Arguments: Coordinates of the place <type: Object>
        Return: Live Temperature
        
        structure of the coordinates object:
            {
                latitude: <type: int>,
                longitude: <type: int>
            }
        
        functionality:
            -extract the latitude, longitude fomr the coordinates object
            -fetches the api key for open weather api from environment variables by passing the lat, long in the fetch url
            -convert temperature to celcius scale
            - return the temperature
    '''
    @staticmethod
    def fetch_live_temp(coordinates):
        # extracting the lat, long
        latitude = coordinates["latitude"]
        longitude = coordinates["longitude"]
        
        # getting key from env file and setting up the url
        OPENWEATHERAPI_KEY=os.getenv("OPENWEATHERAPI_KEY")
        OPENWEATHERAPI_URL=f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={OPENWEATHERAPI_KEY}"

        # Fetching the live temperature
        temperatures_live = requests.get(OPENWEATHERAPI_URL)
        
        # Check if the api call returns a successful status code (200)
        if temperatures_live.status_code == 200:
            data = temperatures_live.json()
            
            # extracting temp and convert into celcius scale
            temperature = data['main']['temp'] - 273.15
            # print and return the temperature
            print(temperature)
            return temperature
        else:
            # Print error message if the fetch status is not 200, ie, error.
            print("Temperature fetch failed, this is most probably an API error")


# Defining the startup functionality of the server
'''
    Function: startup_weather_monitor
    argyments: context,
    returns: none
    
    functinality:
        - save the server address in the environment variables
        - Log a success message along with agent address and agent name
'''
@WeatherMonitor.on_event("startup")
async def startup_weather_agent(ctx: Context):
    os.putenv("SERVER_ADDRESS", ctx.address)

    ctx.logger.info(f"Weather Monitor up and running. The registered name is {ctx.name}, the address {ctx.address}")


# Decorator to define the funtionality of the server on recieving message from the user agent
'''
    Function: server_message_handler
    Arguments: context, sender address, message (along with the protocol)
    Returns: None
    
    functionality:
        - log the recieved data from user
        - fetch the live temperature by calling the fetch_live_temp method of the TemperatureMonitoring class 
        - extracting the min and max temp from the user data passed as 'msg'
        - compare the current temp with the min and max temp and give push notification accordingly.
'''
@WeatherMonitor.on_message(model=MessageToServer)
async def server_message_handler(ctx: Context, sender: str, msg: MessageToServer):
    
    # Log the recieved data
    ctx.logger.info(f"Recieved message from {sender}: Location: {msg.city}, {msg.state}, {msg.country}, min_temp: {msg.min_temp}, max_temp: {msg.max_temp}, coordinates: {msg.geoLocation}") 
    
    # get the current temperature
    live_temperature = TemperatureMonitoring.fetch_live_temp(msg.geoLocation)
    
    # extracting min and max temp provided by the user
    minimum = msg.min_temp
    maximum = msg.max_temp
    
    # If temp is less than than minimum, alert the user of the same
    if live_temperature < minimum:
        user_alert = f"Temperature out of range!"
        notification.notify(
            title = user_alert,
            message = f"Live temperature ({live_temperature}°C) is below minimum provided temperature!",
            app_icon = '',
            timeout = 3, # timeout defines the number of seconds after which the notifcation will fade away
        )
    # If temp is more than the max temp, alert the user.
    elif live_temperature > maximum:
        user_alert = f"Temperature out of range!"
        notification.notify(
            title = user_alert,
            message = f"Live temperature ({live_temperature}°C) is above the maximum provided temperature!",
            app_icon = '',
            timeout = 3,
        )
    # If none of the above, ie, temperature is in the given range, do nothing.
    else:
        user_alert = f"Live temperature inside the given range."

    # Setting up the message to send back the user
    # Contains current_temp <type: int> and out_of_range <type: bool>
    server_response = MonitorResponse(
        current_temp = live_temperature,
        out_of_range=(live_temperature < minimum or live_temperature > maximum)
    )
    
    # Send the message to the user
    await ctx.send(sender, server_response)

if __name__ == "__main__":
    WeatherMonitor.run()


