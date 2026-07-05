import json
from datetime import datetime
from pathlib import Path

DATA = Path("data")
FILE = DATA / "history.json"


class Logger:

    @staticmethod
    def log(message):

        DATA.mkdir(exist_ok=True)

        if FILE.exists():

            try:
                history = json.loads(FILE.read_text())

            except:

                history = []

        else:

            history = []

        history.append({

            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "message": message

        })

        FILE.write_text(
            json.dumps(history, indent=4)
        )