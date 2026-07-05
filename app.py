import os
import threading
import time

from battery import Battery
from config import load
from logger import Logger
from notifier import Notifier
from tray import run


config = load()

ALERT = config["alert_level"]
INTERVAL = config["check_interval"]

alert_sent = False


def monitor():

    global alert_sent

    print("BatteryGuard Started")

    while True:

        status = Battery.get()

        if status is None:

            time.sleep(INTERVAL)

            continue

        percent = status["percent"]

        charging = status["charging"]

        print(percent, charging)

        if charging:

            if percent >= ALERT and not alert_sent:

                Notifier.send(percent)

                Logger.log(
                    f"Alert at {percent}%"
                )

                alert_sent = True

        else:

            alert_sent = False

        time.sleep(INTERVAL)


def exit_app(icon):

    icon.stop()

    os._exit(0)


if __name__ == "__main__":

    threading.Thread(
        target=monitor,
        daemon=True
    ).start()

    run(exit_app)