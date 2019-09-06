from . import ControlModule

class AutomationModule(ControlModule):
    def __init__(self):
        self.module_config = {
            "module_name":"automation",
            "display_name":"Automation",
            "polling_frequency_seconds":30
            }

    def get_data(self):
        print(self.module_config['module_name'])

instance = AutomationModule()
