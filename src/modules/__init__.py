import os

# Module info storage
module_list = []

class ControlModule(object):
    def get_data(self):
        raise NotImplementedError

    class AlertItem(object):
        """ Class for grouping data pertaining to an alert
        """
        def __init__(self, measurand, value, msg=None):
            self.measurand = measurand  # Item being measured
            self.value = value  # Value of measurand
            self.msg = msg  # Alert message (why is this measured value important)

    class ReportItem(object):
        """ Class for grouping data to be included in a report
        """
        def __init__(self, item, value):
            self.item = item  # Item being reported
            self.value = value  # Value of the item

# Initialize placeholder variables, mostly so the linter doesn't complain (value(s) will be populated by code below)
instance = None

# Iterate through all files in this dir and import them
cur_path = os.path.dirname(os.path.abspath(__file__))
for filename in os.listdir(cur_path):
    if filename.endswith(".py") and os.path.join(cur_path, filename) != __file__:  # Only process .py files that aren't this init file
        exec(compile(open(os.path.join(cur_path, filename), 'rb').read(), filename, 'exec'))  # Open the file, compile it, and exec the result
        if instance != None and isinstance(instance, ControlModule):
            module_list.append(instance)
