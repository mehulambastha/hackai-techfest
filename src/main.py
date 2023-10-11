# Team #
# Members
# Mehul Ambastha
# Sumit Dhiman,
# Ayan Choradia,
# Divyansh Tripathi


# Importing important components frmo ugents module
from uagents import Bureau

# importing the user agent
from agents.user import User

# importing the Weather Monitor agent (server)
from agents.monitoringServer import WeatherMonitor

# initialised the bureau
bureau = Bureau()

# Adding both the agents to bureau
bureau.add(WeatherMonitor)
bureau.add(User)

# Running the bureau
if __name__ == "__main__":
    bureau.run()