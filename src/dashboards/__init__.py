import os

# Dashboard info storage
_dash_list = []

# Abstraction class used to consolidate dashboard update calls
class _DashAbstraction():
    def __init__(self, dashes):
        self.dashes = dashes
    def update_weather(self, data):
        for dash in self.dashes: dash.update_weather(data)
    def update_home(self, data):
        for dash in self.dashes: dash.update_home(data)
    def update_misc(self, data):
        for dash in self.dashes: dash.update_misc(data)

class Dashboard(object):
    def update_weather(self, data):
        raise NotImplementedError
    def update_home(self, data):
        raise NotImplementedError
    def update_misc(self, data):
        raise NotImplementedError


# Initialize placeholder variables, mostly so the linter doesn't complain (value(s) will be populated by code below)
_instance = None

# Iterate through all files in this dir and import them
cur_path = os.path.dirname(os.path.abspath(__file__))
for filename in os.listdir(cur_path):
    if filename.endswith(".py") and os.path.join(cur_path, filename) != __file__:  # Only process .py files that aren't this init file
        exec(compile(open(os.path.join(cur_path, filename), 'rb').read(), filename, 'exec'))  # Open the file, compile it, and exec the result
        if _instance != None and isinstance(_instance, Dashboard):
            _dash_list.append(_instance)

dashboard = _DashAbstraction(_dash_list)
