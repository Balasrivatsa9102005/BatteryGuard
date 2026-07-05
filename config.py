import json
from pathlib import Path
from events import bus


CONFIG_PATH = Path("data/config.json")


class Config:

    def __init__(self):
        self._load()

    def _load(self):
        if not CONFIG_PATH.exists():
            self.data = {
                "alert_level": 80,
                "check_interval": 5
            }
            self._save()
        else:
            with open(CONFIG_PATH, "r") as f:
                self.data = json.load(f)

    def _save(self):
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.data, f, indent=4)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self._save()
        
        print(f"[DEBUG] Config.set() called with key={key}, value={value}")
        print(f"[DEBUG] Number of listeners: {len(bus.listeners.get('config_changed', []))}")
        
        # Emit event
        bus.emit("config_changed", {
            "key": key,
            "value": value
        })
        print("[DEBUG] Event emitted successfully")

    def all(self):
        return self.data

    # Add these methods for dictionary-style access
    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self.data

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def items(self):
        return self.data.items()


# singleton instance
config = Config()


def load():
    return config