""" Provides a way to detect activity in a folder"""

import time
import os
import watchdog.events
import watchdog.observers

# import search_match
import process_file

# Create a Class that will handle the event of a document being added
# in the specific directory using the Watchdog library

""" This is the class that will handle all the processing steps """

class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler. In our case it is '*.csv'
        watchdog.events.PatternMatchingEventHandler.__init__(
            self, patterns=["*.xlsx"], ignore_directories=True, case_sensitive=False
        )

    def on_created(self, event):
        print("Watchdog received created event - % s." % event.src_path)
        # Event is created, you can process the new file
        # Give the copy process time to complete.
        time.sleep(3)
        search_complete = True
        # search_complete = True
        if search_complete:
            process_activity = process_file.process_file(event.src_path)
        if process_activity:
            print("Application exiting")
            os._exit(0)


# Turn the Watchdog on. Create an instance of the Handler class once the script is launched.
# The processing of the xlsx file and tables will also be handled from within the class instance.

if __name__ == "__main__":
    src_path = r"\\esbmft01\ESB_Fusion\INBOUND\Tableau\Login"
    event_handler = Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)

    observer.start()
    print("Watchdog running")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
