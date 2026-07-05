from pathlib import Path
import threading
import time
import pystray
from PIL import Image
from settings_ui import open_settings
from config import load

ICON_PATH = Path("assets/icon.png")
ICON_HIGH = Path("assets/icon_high.png")
ICON_MED = Path("assets/icon_med.png")
ICON_LOW = Path("assets/icon_low.png")

_tray_icon = None
_current_status = {
    "percent": None,
    "charging": None
}

config = load()

def get_icon(percent):
    """Return appropriate icon based on battery percentage"""
    if percent is None:
        return Image.open(ICON_PATH)
    elif percent >= 60:
        return Image.open(ICON_HIGH)
    elif percent >= 20:
        return Image.open(ICON_MED)
    else:
        return Image.open(ICON_LOW)

def update_status(percent, charging):
    _current_status["percent"] = percent
    _current_status["charging"] = charging
    
    # Update tray icon based on battery level
    if _tray_icon is not None and percent is not None:
        icon = get_icon(percent)
        _tray_icon.icon = icon

def _update_loop():
    global _tray_icon
    while _tray_icon is not None:
        percent = _current_status["percent"]
        charging = _current_status["charging"]
        if percent is not None:
            status = "Charging ⚡" if charging else "Discharging 🔋"
            _tray_icon.title = f"BatteryGuard | {percent}% | {status}"
            
            # Update icon dynamically
            icon = get_icon(percent)
            _tray_icon.icon = icon
            
        time.sleep(2)

def run(on_exit):
    global _tray_icon
    
    # Start with default icon
    image = Image.open(ICON_PATH)
    
    def toggle_alert(icon, item):
        current = config.get("alert_level")
        new_value = 60 if current == 80 else 80
        config.set("alert_level", new_value)
        print(f"[Tray] Alert Level → {new_value}")

    def show_status(icon, item):
        p = _current_status["percent"]
        c = _current_status["charging"]
        print(f"[STATUS] {p}% | {'Charging' if c else 'Discharging'}")

    _tray_icon = pystray.Icon(
        "BatteryGuard",
        image,
        "Battery Guard",
        menu=pystray.Menu(
            pystray.MenuItem(
                lambda text: f"Alert Level: {config.get('alert_level')}%",
                lambda icon, item: None,
                enabled=False
            ),
            pystray.MenuItem(
                "Settings",
                lambda icon, item: open_settings()
            ),
            pystray.MenuItem(
                "Toggle Alert Level",
                toggle_alert
            ),
            pystray.MenuItem(
                "Show Status",
                show_status
            ),
            pystray.MenuItem(
                "Exit",
                lambda icon, item: on_exit(icon)
            )
        )
    )

    threading.Thread(target=_update_loop, daemon=True).start()
    _tray_icon.run()