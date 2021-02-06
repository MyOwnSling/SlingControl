import os
import json
import time
from pushbullet import Pushbullet as pb


def cooldown(notify_func):
    """
    Check to see if the given notification title has been sent within
     the configured cooldown window
    """

    def _cooldown_wrapper(self, *args, **kwargs):

        # We know the title is always going to be the first arg
        title = args[0]

        # Check to see if this notification has been sent at all
        if not title in self.alert_records:
            self.alert_records[title] = time.time()
            return notify_func(self, *args, **kwargs)
        
        # Get the time since last notification and check it against the cooldown window
        span = time.time() - self.alert_records[title]
        if span > self.cooldown:
            self.alert_records[title] = time.time()
            return notify_func(self, *args, **kwargs)

        # Cooldown hasn't expired; do nothing
        return

    return _cooldown_wrapper

class PBNotifier():
    def __init__(self, registrants):
        if not "PB_AUTH" in os.environ:
            raise ValueError("Missing PushBullet auth token")
        self.pb_client = pb(os.environ["PB_AUTH"])
        self.pb_chats = dict()

        # Cooldown values used to keep repeated alerts
        self.cooldown = 120 * 60 # Cooldown in seconds
        self.alert_records = dict()  # Track alert titles and the last alert time

        # Expect a dictionary with 'pb' key whose value is an array of registrant emails
        try:
            self.registrants = json.loads(registrants)['pb']
        except (KeyError, TypeError):
            # The expected key isn't in the dictionary or the dictionary doesn't exist, so we can't continue
            raise KeyError('Registrants dictionary is None or missing required "pb" key')

        # Record each existing chat that corresponds to a registrant
        for chat in self.pb_client.chats:
            if chat.email in self.registrants:
                self.pb_chats[chat.email] = chat
        
        # Take emails and create any chats that don't exist yet
        for registrant in self.registrants:
            if registrant not in self.pb_chats:
                chat = self.pb_client.new_chat(registrant, registrant)
                self.pb_chats[chat.email] = chat


    @cooldown
    def notify(self, title, msg, recipients=None):
        """Notify the given reicpients (recipient is a destination email)"""

        # If None is provided, send to self only. Also send to self if sending to "all"
        if recipients is None or recipients is 'all':
            self.pb_client.push_note(title, msg)
            if recipients is None: return()

        # If sending to all, set recipients to full list
        if recipients is 'all':
            recipients = self.registrants

        # Send to all recorded recipients
        for recipient in recipients:
            self.pb_chats[recipient].push_note(title, msg)

notifier_class = PBNotifier
