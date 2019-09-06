import os
import time
from threading import Thread
from queue import Queue

from modules import module_list, ControlModule

def run_job(module_instance, queue):
    """
    Function used to wrap module functions for threading
    """

    if not isinstance(module_instance, ControlModule):
        raise ValueError("Instance not of type {}".format(repr(ControlModule)))

    # Record polling period into new, easier to reference var
    period = module_instance.module_config['polling_period_seconds']

    # Main thread loop
    while True:
        # Record start time before calling the real runction
        start_time = time.time()

        # Do some work
        data = module_instance.get_data()  # Real work happens here (module data gathering)
        queue.put((module_instance.module_config, data, time.strftime("%H.%M.%S")))

        # Record the elapsed (real) time and sleep for any remaining time in our period. 
        # This technique allows us to execute roughly "every x seconds" as opposed to 
        # "waiting x seconds before running again"
        elapsed = time.time() - start_time
        if elapsed < period:
            time.sleep(period - elapsed)


def handle_data(data):
    """
    Placeholder data handler. Eventually, this should take the given data
     and pass it on to the UI and/or other relevant location, potentially
     based on the nature of the data.
    """
    print(data)


def main():

    # Setup threading resources
    thread_pool = []  # Array used to store our threads (one thread per module)
    data_queue = Queue()  # Thread-safe queue used to process data sent back from the threads

    # Create a thread for each module and start it
    for module in module_list:
        thread = Thread(target=run_job, args=(module, data_queue), name=module.module_config["module_name"])
        thread.start()
        thread_pool.append(thread)
    
    # Monitoring and queue handling
    while True:
        data_item = data_queue.get()
        handle_data(data_item)

main()
