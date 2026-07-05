# 🔋 BatteryGuard

BatteryGuard is a lightweight desktop utility that monitors your laptop's battery status in the background and alerts you when the battery reaches a user-defined charging limit. It runs from the system tray, helping users avoid overcharging and maintain better battery health.

---

## ✨ Features

* 🔋 Real-time battery monitoring
* 🔔 Desktop notification when the battery reaches the configured limit
* ⚙️ Configurable battery alert percentage
* ⏱️ Adjustable battery check interval
* 🖥️ System tray integration
* 📝 Battery event logging
* 💾 Persistent settings stored in `config.json`
* 🔄 Live configuration updates without restarting the application

---

## 📂 Project Structure

```text
BATTERYGUARD/
│
├── assets/                 # Icons and UI assets
├── data/
│   └── config.json         # Application configuration
│
├── app.py                  # Application entry point
├── battery.py              # Battery information provider
├── config.py               # Configuration manager
├── events.py               # Event bus for live updates
├── logger.py               # Logging module
├── monitor.py              # Battery monitoring logic
├── notifier.py             # Desktop notification service
├── settings_ui.py          # Settings window
├── tray.py                 # System tray integration
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

* Python 3.10+
* psutil
* pystray
* Pillow
* plyer
* CustomTkinter

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/BatteryGuard.git
cd BatteryGuard
```

Create a virtual environment:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Start BatteryGuard using:

```bash
python app.py
```

The application will start in the background and place an icon in the system tray.

---

## ⚙️ Configuration

Settings are stored in:

```text
data/config.json
```

Example:

```json
{
    "alert_level": 80,
    "check_interval": 300
}
```

| Setting          | Description                                                        |
| ---------------- | ------------------------------------------------------------------ |
| `alert_level`    | Battery percentage at which a notification is shown while charging |
| `check_interval` | Time (in seconds) between battery checks                           |

Settings can also be modified through the application's Settings window.

---

## 🏗️ Architecture

```text
Battery
   │
   ▼
BatteryMonitor
   │
   ├────────► Tray UI
   │
   ├────────► Notification Service
   │
   ├────────► Logger
   │
   ▼
Configuration Manager
   │
   ▼
config.json
```

---

## 📌 Future Enhancements

* Dynamic tray icons based on battery level
* Auto-start on system boot
* Battery usage history and analytics
* Export battery logs
* Multiple notification profiles
* Cross-platform packaging
* Modern dashboard interface

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push to your branch.
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Panigrahi Bala Srivatsa**

* B.Tech CSE (AI & ML), VIT-AP University
* Passionate about Machine Learning, Artificial Intelligence, and Software Development.

If you found this project useful, consider giving it a ⭐ on GitHub.
