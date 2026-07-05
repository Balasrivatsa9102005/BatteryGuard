import os
import threading
import time

from battery import Battery
from config import load
from logger import Logger
from notifier import Notifier
from tray import run
from events import bus  # Add this


config = load()

# Use get() method or config["alert_level"] now works
ALERT = config.get("alert_level")  # or config["alert_level"]
INTERVAL = config.get("check_interval")  # or config["check_interval"]

alert_sent = False


def monitor():
    global alert_sent, ALERT, INTERVAL
    
    print("BatteryGuard Started")
    print(f"Alert Level: {ALERT}%, Check Interval: {INTERVAL}s")

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
                Logger.log(f"Alert at {percent}%")
                alert_sent = True
        else:
            alert_sent = False

        time.sleep(INTERVAL)


# Listen for config changes
def on_config_change(data):
    global ALERT, INTERVAL
    
    if data["key"] == "alert_level":
        ALERT = data["value"]
        print(f"[Monitor] Alert level updated to: {ALERT}%")
    elif data["key"] == "check_interval":
        INTERVAL = data["value"]
        print(f"[Monitor] Check interval updated to: {INTERVAL}s")

# Subscribe to config changes
bus.subscribe("config_changed", on_config_change)


def exit_app(icon):
    icon.stop()
    os._exit(0)


if __name__ == "__main__":
    threading.Thread(target=monitor, daemon=True).start()
    run(exit_app)