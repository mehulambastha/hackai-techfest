# Temperature Alert System

The Temperature Alert System is a versatile tool that makes real-time temperature monitoring and notifications easy. Whether you're an outdoor enthusiast, a traveler, or just someone who likes to stay informed about the weather, this project is designed to meet your needs. It also features a fully functional GUI to make it easier for the users to interact with the project. Here's what you can expect from the Temperature Alert System:

## Key Features

- **Real-time Temperature Data**: The system connects to a free weather API to fetch current temperature information for your selected location.

- **Customizable Temperature Thresholds**: You have the flexibility to set both minimum and maximum temperature thresholds, allowing you to receive alerts tailored to your preferences.

- **Instant Notifications**: Receive immediate alerts and notifications when the current temperature in your chosen location falls below or exceeds your predefined thresholds.

- **GUI for user input**: Users can enter data through a light GUI window developed in Tkinter library of python.



## Getting Started

### Prerequisites

Before you start using the Temperature Alert System, make sure you have the following prerequisites in place:

Make sure you have python installed in your system by running python --version on your terminal.
We recommend using Python 3.8 or higher.

- **Poetry**: Poetry is a packaging and dependency management tool for Python. If you don't have Poetry installed, you can follow the installation instructions [here](https://python-poetry.org/docs/#installation).


### Cloning the Project
Run the command on your terminal 
```bash git clone https://github.com/mehulambastha/hackai-techfest-230588/```


#### API Keys

To fully utilize the Temperature Alert System, you'll need API keys from the following sources:

#### OpenWeather API

1. Visit [OpenWeather](https://openweathermap.org/) 
Create an account on OpenWeatherMap and get an Api Key.

How to get an API key from OpenWeather-

Visit OpenWeatherMap and create a new account or Sign-in to your account.

Select My API keys and generate an API Key

Now copy the key.

For more queries visit API documentation .

2. Retrieve your API key from the dashboard. Ensure you have access to the "Current Weather" data.

#### API Ninjas

1. Visit [API Ninjas](https://apininjas.com/) and sign up or log in.

2. Obtain your API key from the dashboard, specifically from the "Geocoding API" section.

#### UAgents Server Address

You'll also need the server address for uAgents. Detailed information on obtaining this address can be found in the documentation at [Uagents Doc](https://uagents-doc.example.com/).

Once you have these API keys and your server address, create a `.env` file within the `src` directory with the following content:

```bash
 OPENWEATHERAPI_KEY="{YOUR OPEN WEATHER API KEY}"
 APININJA_KEY="{YOUR API NINJAS GEOCODING API KEY}"
 SERVER_ADDRESS="{YOUR SERVER ADDRESS}"
```

Note: when putting the APININJA_KEY, enclose the key in quotation marks ("). This is so that the key parses correctly, as it contains characters like equal signs (=). 

Note: the GUI Window is made using tkinter library, it is must to have it. Most [ython installations have tkinter pre-installed, but in case your system does not have it, install tkinter using-

```bash 
pip install tk
```

### Installation and Setup

Now, let's set up and run the Temperature Alert System:

```bash
# Install project dependencies
poetry install

# Activate the virtual environment
poetry shell

# Install additional requirements
pip install -r requirements.txt
```

To launch the project and its agents, navigate to the `src` directory and execute the main script:

```bash
cd src
python3 main.py
```

Congratulations! You are now ready to start receiving temperature alerts and keeping a watchful eye on the weather with the Temperature Alert System. Stay informed and stay comfortable!
