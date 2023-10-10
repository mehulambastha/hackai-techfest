from uagents import Bureau
from agents.user import User
from agents.monitoringServer import WeatherMonitor

bureau = Bureau()
bureau.add(WeatherMonitor)
bureau.add(User)

if __name__ == "__main__":
    bureau.run()