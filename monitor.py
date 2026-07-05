import time
from battery import Battery
from tray import update_status
from events import bus


class BatteryMonitor:

    def __init__(self, config, notifier, logger):

        self.notifier = notifier
        self.logger = logger

        # 🔥 live state (updated via events)
        self.alert_level = config.get("alert_level")
        self.interval = config.get("check_interval")

        self.alert_sent = False

        # 🔌 subscribe to config updates
        bus.subscribe("config_changed", self.on_config_change)

    def on_config_change(self, data):

        if data["key"] == "alert_level":
            self.alert_level = data["value"]

        elif data["key"] == "check_interval":
            self.interval = data["value"]

        print(f"[Monitor] Updated → {data['key']} = {data['value']}")

    def run(self):

        print("BatteryGuard Monitor Started")

        while True:

            status = Battery.get()

            if status is None:
                time.sleep(self.interval)
                continue

            percent = status["percent"]
            charging = status["charging"]

            print(percent, charging)

            # 🔌 update tray
            update_status(percent, charging)

            # ⚡ alert logic (uses LIVE updated value)
            if charging:

                if percent >= self.alert_level and not self.alert_sent:

                    self.notifier.send(percent)
                    self.logger.log(f"Alert at {percent}%")

                    self.alert_sent = True

            else:
                self.alert_sent = False

            time.sleep(self.interval)