import datetime
import time
import sys

import location
import notifications


def get_latest_gps_data():

    count = 0
    while True:
        now = datetime.datetime.now()

        location.accuracy = location.LOCATION_ACCURACY_BEST

        location.start_updating()
        time.sleep(0.5)
        longitude, latitude, altitude = location.get_location()
        location.stop_updating()

        loc = {"longitude": longitude,
               "latitude": latitude,
               "altitude": altitude,
               "timestamp": str(datetime.datetime.now())}

        timestamp = loc['timestamp']
        dt = abs((now - timestamp).total_seconds())
        if dt < 10:
            break
        if count == 5:
            message = notifications.Notification(message='System Exit Beacause of Delay: {}'.format(dt))
            notifications.schedule_notification(message, delay=0, repeat=False)
            sys.exit()
        print('GPS Loop={}'.format(count))
        count += 1
    return loc
