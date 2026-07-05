from plyer import notification


class Notifier:

    @staticmethod
    def send(percent):
        notification.notify(
            title="🔋 Battery Guard",
            message=f"Battery reached {percent}%.\nPlease unplug the charger.",
            timeout=10,
        )