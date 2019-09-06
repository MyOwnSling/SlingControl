from . import ControlModule

class HomeStatusModule(ControlModule):
    def __init__(self):
        self.module_config = {
            "module_name":"homestatus",
            "display_name":"Home Status",
            "polling_frequency_seconds":10
            }

    def get_data(self):
        print(self.module_config['polling_frequency_seconds'])

instance = HomeStatusModule()
