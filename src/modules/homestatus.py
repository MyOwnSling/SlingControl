from . import ControlModule

class HomeStatusModule(ControlModule):
    def __init__(self):
        self.module_config = {
            "module_name":"homestatus",
            "display_name":"Home Status",
            "polling_period_seconds":10
            }

    def get_data(self):
        return "PLACEHOLDER home status data"

instance = HomeStatusModule()
