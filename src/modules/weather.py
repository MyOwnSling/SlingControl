from . import ControlModule

class WeatherModule(ControlModule):
    def __init__(self):
        self.module_config = {
            "module_name":"weather",
            "display_name":"Weather",
            "polling_frequency_seconds":1800
            }

    def get_data(self):
        print(self.module_config['display_name'])

instance = WeatherModule()
