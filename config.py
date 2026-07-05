import json
from pathlib import Path

DATA = Path("data")
CONFIG = DATA / "config.json"

DEFAULT = {
    "alert_level": 80,
    "check_interval": 60
}


def load():

    DATA.mkdir(exist_ok=True)

    if not CONFIG.exists():

        CONFIG.write_text(
            json.dumps(DEFAULT, indent=4)
        )

        return DEFAULT

    return json.loads(CONFIG.read_text())


def save(config):

    CONFIG.write_text(
        json.dumps(config, indent=4)
    )