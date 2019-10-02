import os 

notifier_list = []

# class Notifier:
#     def notify(self, title, msg, recipients=None):
#         raise NotImplementedError

# Initialize placeholder variables, mostly so the linter doesn't complain (value(s) will be populated by code below)
notifier_class = object

# Get config from environment
if not "RECIPIENTS" in os.environ:
    raise ValueError("Missing list of notification recipients")
_receipients = os.environ["RECIPIENTS"]

# Iterate through all files in this dir and import them
cur_path = os.path.dirname(os.path.abspath(__file__))
for filename in os.listdir(cur_path):
    if filename.endswith(".py") and os.path.join(cur_path, filename) != __file__:  # Only process .py files that aren't this init file
        exec(compile(open(os.path.join(cur_path, filename), 'rb').read(), filename, 'exec'))  # Open the file, compile it, and exec the result
        if notifier_class != None:# and isinstance(notifier_class, Notifier):
            notifier_list.append(notifier_class(_receipients))