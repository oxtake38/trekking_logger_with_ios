import os
import pickle
import datetime
import time
import sys
import pathlib

import notifications

sys.path.append(pathlib.Path(__file__).parent)

from src import util, calculation, location_api

DIR = "log"
PATH = 'tmp.pkl'


def main():
    os.makedirs(DIR, exist_ok=True)
    # Get Old data
    now = datetime.datetime.now()
    is_first = False

    if not os.path.exists(os.path.join(DIR, PATH)):
        is_first = True
    else:
        with open(os.path.join(DIR, PATH), 'rb') as f:
            log = pickle.load(f)
        if abs(now - log[-1]['timestamp']).total_seconds() > 60 * 20:
            # notification.schedule("Reset Logger")
            message = notifications.Notification(message="Reset Logger")
            notifications.schedule_notification(message, delay=0, repeat=False)
            time.sleep(1)
            os.rename(os.path.join(DIR, PATH), now.strftime('%Y-%m-%d_%H-%M-%S'))
            del log
            is_first = True

    # GPSログの取得
    latest_data = location_api.get_latest_gps_data()

    if not is_first:
        log.append(latest_data)
        for i in range(len(log)):
            if i != 0:
                log[i]["distance"] = calculation.calc_distance({"longitude": log[i]["longitude"], "latitude": log[i]["latitude"]},
                                                               {"longitude": log[i - 1]["longitude"], "latitude": log[i - 1]["latitude"]},)
            else:
                log[i]["distance"] = 0

        # 現在から36, 66分を超えるデータをそれぞれ抽出
        log_30 = [log[i - 1] for i in range(len(log), 0, -1) if abs((log[-1]['timestamp'] - log[i - 1]['timestamp']).total_seconds()) < 36 * 60][::-1]
        log_60 = [log[i - 1] for i in range(len(log), 0, -1) if abs((log[-1]['timestamp'] - log[i - 1]['timestamp']).total_seconds()) < 66 * 60][::-1]
        # 現在から66分を超えるデータはpklから除外する
        log = log_60
        # "10:10:24 +3"
        string = '{}:{}:{}'.format(str(now.hour).zfill(2), str(now.minute).zfill(2), str(now.second).zfill(2))
        string += '\n'
        string += '+{}'.format(util.get_time_diff_str((log_30[-1]['timestamp'] - log_30[-2]['timestamp']).total_seconds()))
        string += '\n'
        string += '--Diff--\n'
        string += 'Alt {:.0f}m'.format(log_30[-1]['altitude'] - log_30[-2]['altitude'])
        string += '\n'
        string += 'Dist {:.2f}km'.format(log_30[-1]['distance'])
        string += '\n'
        string += '--Current--\n'
        string += 'Alt {:.0f}m'.format(log_30[-1]['altitude'])
        string += '\n'
        string += '\n'
        string += '--30min--\n'
        string += 'V {:.0f}m/h'.format(calculation.calc_speed((log_30[-1]['timestamp'] - log_30[0]['timestamp']).total_seconds(),
                                                              log_30[-1]['altitude'],
                                                              log_30[0]['altitude']),)
        string += '\n'
        string += 'H {:.2f}km/h\n'.format(sum([m['distance'] for m in log_30]) * 3600 / (log_30[-1]['timestamp'] - log_30[0]['timestamp']).total_seconds(),)
        string += '\n'
        string += '--60min--\n'
        string += 'V {:.0f}m/h'.format(calculation.calc_speed((log_60[-1]['timestamp'] - log_60[0]['timestamp']).total_seconds(),
                                                              log_60[-1]['altitude'],
                                                              log_60[0]['altitude']),)
        string += '\n'
        string += 'H {:.2f}km/h\n'.format(sum([m['distance'] for m in log_60]) * 3600 / (log_60[-1]['timestamp'] - log_60[0]['timestamp']).total_seconds(),)

        message = notifications.Notification(message=string)
        notifications.schedule_notification(message, delay=0, repeat=False)

    else:
        latest_data["distance"] = 0
        log = [latest_data]
        string = '{}:{}:{}'.format(str(now.hour).zfill(2), str(now.minute).zfill(2), str(now.second).zfill(2))
        string += '\n'
        string += '--Current--\n'
        string += 'Alt {:.0f}m'.format(log[-1]['altitude'])

        message = notifications.Notification(message=string)
        notifications.schedule_notification(message, delay=0, repeat=False)

    with open(os.path.join(DIR, PATH), 'wb') as f:
        pickle.dump(log, f)


if __name__ == '__main__':
    main()
