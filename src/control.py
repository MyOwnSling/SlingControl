import os
import time
import sys
from threading import Thread
from queue import Queue

from dashboards import dashboard
from modules import module_list, ControlModule
try:
    from notifiers import notifier_list
except ValueError as vex:
    print("Notifier error: " + str(vex), file=sys.stderr)

class JobReturn():
    def __init__(self, module_config, return_data, queue_time):
        self.modlue_config = module_config
        self.return_data = return_data
        self.queue_time = queue_time


def run_job(module_instance, queue):
    """ Function used to wrap module functions for threading
    """

    # We can't process something that isn't a control module
    if not isinstance(module_instance, ControlModule):
        raise ValueError("Instance not of type {}".format(repr(ControlModule)))

    # Record polling period into new, easier to reference var
    period = module_instance.module_config['polling_period_seconds']
    if period <= 0:  # Allow for disabling of a module
        return

    # Main thread loop
    while True:
        # Record start time before calling the real runction
        start_time = time.time()

        # Do some work
        try:
            data = module_instance.get_data()  # Real work happens here (module data gathering)
            job_data = JobReturn(module_instance.module_config, data, time.strftime("%Y.%m.%d-%H.%M.%S", time.localtime(start_time)))
            queue.put(job_data)
        except ValueError as vex:
            print("Module error: " + str(vex), file=sys.stderr)
        

        # Record the elapsed (real) time and sleep for any remaining time in our period. 
        # This technique allows us to execute roughly "every x seconds" as opposed to 
        # "waiting x seconds before running again"
        elapsed = time.time() - start_time
        if elapsed < period:
            time.sleep(period - elapsed)


def handle_data(data):
    """
    Module data handler that takes data sent from a running module and calls any 
     notifiers if alert text has been populated by a module while also supplying 
     updates to any dashboards.
    """

    # data.return_data: a ReturnItem object in ControlModule
    module_data = data.return_data
    alert_items = None
    try:
        alert_items = module_data.interpreter(module_data.data, dashboard)
    except Exception as ex:
        print("Data interpreter error: " + str(ex), file=sys.stderr)
        return

    for alert in alert_items:
        print("ALERT: {} ({}) - {}".format(alert.measurand, alert.value, alert.msg))
        try:
            for notifier in notifier_list:
                notifier.notify(alert.measurand, "{}{}{}".format(alert.value, os.linesep, alert.msg))
        except ValueError as vex:
            print("Notifier error: " + str(vex), file=sys.stderr)


def main():

    # Setup threading resources
    thread_pool = []  # Array used to store our threads (one thread per module)
    data_queue = Queue()  # Thread-safe queue used to process data sent back from the module threads

    # Create a thread for each module and start it
    for module in module_list:
        print("Loading {}".format(module.module_config["display_name"]))
        thread = Thread(target=run_job, args=(module, data_queue), name=module.module_config["module_name"])
        thread.start()
        thread_pool.append(thread)
    
    # Monitoring and queue handling
    while True:
        data_item = data_queue.get()
        try:
            handle_data(data_item)
        except Exception as ex:
            print(ex, file=sys.stderr)

if __name__ == "__main__":
    main()
