from pathlib import Path

import pystray
from PIL import Image


ICON = Path("assets/icon.png")


def run(on_exit):

    image = Image.open(ICON)

    icon = pystray.Icon(

        "BatteryGuard",

        image,

        "Battery Guard",

        menu=pystray.Menu(

            pystray.MenuItem(
                "Exit",
                lambda icon, item: on_exit(icon)
            )

        )
    )

    icon.run()