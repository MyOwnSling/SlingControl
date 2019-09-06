from . import ControlModule

class WeatherModule(ControlModule):
    def __init__(self):
        self.module_config = {
            "module_name":"weather",
            "display_name":"Weather",
            "polling_period_seconds":60
            }

    def get_data(self):
        return "PLACEHOLDER weather data"

instance = WeatherModule()
