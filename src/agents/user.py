from uagents import Agent, Context, Model
import os
from messages.messageModels import MessageToServer, MonitorResponse
import requests
import json
import app
from dotenv import load_dotenv
load_dotenv()

#Set up tkinter app
tkinter_app = app.create_tkinter_app()


# Setup the user agent
User = Agent(
    name= "User agent",
    port= 8002,
    seed="User inputs",
    endpoint={
        "http://127.0.0.1:8002/user": {},
    }
)

# The startup functionalities of the User Agent
@User.on_event("startup")
async def startup_user_agent(ctx: Context):
    # Print a simple success message with user agent address and its name.
    ctx.logger.info(f"User agent is running succesfully.\n\tAddress: {ctx.address}\n\tName: {ctx.name}")
    
    
# User Data <type: Object>
# Contents
'''
    city <type: str>,
    state <type: str>, 
    country <type: str>, 
    min_temp <type: float>, 
    max_temp <type: float>, 
    coordinates <type: Object> -> { latitude, longitude }
'''
# get user inputs from tkinter app
user_data = app.get_tkinter_inputs()
user_data["coordinates"] = {}

# Class for dealing with city, state, country and coordinates. 
# Contains method for returning latitude and longitude
class InfoGeoLocation:
    '''
        Function: extract_latlong
        Arguments: None
        Returns:
            Latitude and Longitude
        
        How does it do it?
            - extracts city, state and country from user_data
            - Fetches geoCoding API from API-Ninjas by giving it city and country (and not state because the API does not take state)
            - API Fetch returns complete location details: name, city, state, country, latitude and longitude
            - Operate on the response: match city and state -> extract just the latitude and longitude
            - saves the lat,long in user_data under "coordinates" key
            - returns the "coordinates" property of user_data

    '''
    @staticmethod
    def extract_latLong():

        # The API Url of API-Ninjas
        api_url = 'https://api.api-ninjas.com/v1/geocoding?city={}&country={}'.format(user_data["city"], user_data["country"])

        # Get the API KEY from environment variables
        API_KEY=os.getenv("APININJA_KEY")
        # Response from the API
        response = requests.get(api_url, headers={'X-Api-Key': API_KEY})

        # Check if the fetch status was successful, ie, whether the resposnse status code is 200 (success)
        if response.status_code == 200: 

            # Format the response text as JSON
            json_formatted_response = json.loads(response.text)

            '''
                The response from API Fetch is of the following format
                [
                    {
                        "name": "London",
                        "latitude": 51.5085,
                        "longitude": -0.1257,
                        "country": "GB"
                    }
                ]
                Sample taken from: https://api-ninjas.com/api/geocoding

                Functionality of the for loop given below:
                    - iterates over the objects returned
                    - matches the country, state, and city name from the JSON response with the country, state and city given by user.
                    - set the latitude and longitude properties of coordinates property of user_data
                    - break the loop
            '''
            for location in json_formatted_response:
                
                # Matching the location in JSON response with user input
                if (location.get("country").lower() == user_data["country"] and location.get("state").lower() == user_data["state"] and location.get("name").lower() == user_data["city"]):
                    
                    # setting the coordinates
                    user_data["coordinates"]["latitude"] = location.get("latitude")
                    user_data["coordinates"]["longitude"] = location.get("longitude")
                    break
            
            # Return the coordinates of user_data ONLY IF the latitude and longitude are NOT NONE
            if user_data["coordinates"]['latitude'] is not None and user_data["coordinates"]['longitude'] is not None:
                    return user_data["coordinates"]
            else:
                print("Coordinates for given location not found")  
                # Otherwise return NONE and NONE for latitude and longitude both
                return {"latitude": None, "longitude": None}

        else:
            # Print the error if the API Call returns errors
            print("Error:", response.status_code, response.text)            



# Keeping it outside the on_interval decorator because there is no need to fetch it every five seconds. The server address remains same during the whole lifetime of one instance 
SERVER_ADDRESS=os.getenv("SERVER_ADDRESS")

# On interval decorator
'''
    Function: send_data_to_server
    Arguments: context
    Returns: None
    
    Usage:
        - extracts latitude and longitude by using extract_latlong method of the InfoGeoLocation class
        - send the complete user data along with latitude and longitude (in a single coordinates object) to the server.
        - the structure of the coordinates object is
            {
                latitude: float
                longitude: float
            }
'''
@User.on_interval(period=5)
async def send_data_to_server(ctx: Context):
    geoLocation = InfoGeoLocation.extract_latLong()
    
    # Sending the data to server according to the MessageToServer protocol
    await ctx.send(SERVER_ADDRESS, MessageToServer(city=user_data["city"], state=user_data["state"], country=user_data["country"], min_temp=user_data["min_temp"], max_temp=user_data["max_temp"], geoLocation=user_data["coordinates"]))


# Decorator to define the user agent's response on reciveing a message fomr the server
'''
    Function: weather_monitor_response
    Arguments: MonitorResponse data model
    Returns: None
    
    functionality:
        - logs the response from the server
        - the response contains two things: current_temp <type: float> and out_of_range <type: bool>
'''
@User.on_message(model=MonitorResponse)
async def weather_monitor_response(ctx: Context, sender: str, msg: MonitorResponse):
    ctx.logger.info(f"Response from server address {sender}:\n Current Temp: {msg.current_temp}\nOut of range? {msg.out_of_range}")