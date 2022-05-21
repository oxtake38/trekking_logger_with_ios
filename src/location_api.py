import datetime
import time
import sys

def get_latest_gps_data():
    import location
    import notification
    count = 0
    while True:
        now = datetime.datetime.now()
        location.start_updates()
        time.sleep(0.5)
        loc = location.get_location()
        location.stop_updates()

        timestamp = loc['timestamp']
        timestamp = datetime.datetime.fromtimestamp(timestamp)
        dt = abs((now - timestamp).total_seconds())
        if dt < 10:
            break
        if count == 5:
            notification.schedule('System Exit Beacause of Delay: {}'.format(dt))
            sys.exit()
        print('GPS Loop={}'.format(count))
        count += 1
    return loc