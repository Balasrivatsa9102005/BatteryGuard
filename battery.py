import psutil


class Battery:

    @staticmethod
    def get():
        battery = psutil.sensors_battery()

        if battery is None:
            return None

        return {
            "percent": battery.percent,
            "charging": battery.power_plugged
        }