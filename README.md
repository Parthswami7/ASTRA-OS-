# A.S.T.R.A OS

**Automated System Tracking & Response Agent**

A.S.T.R.A is a self-hosted, offline operating system overlay that transforms a standard Windows PC into an autonomous, cinematic AI powerhouse. Designed with a Hollywood-grade Tkinter HUD, it actively monitors hardware, optimizes performance, and secures your system using biometric facial recognition—all while keeping your data 100% private and on-device.

---

## 🚀 Key Features

* **Total Privacy (Offline First):** A.S.T.R.A operates entirely on your local hardware. There is no cloud data harvesting, no telemetry sent to third-party servers, and complete data sovereignty.
* **Initiative Protocol (Auto-Optimization):** Actively monitors hardware load. If RAM or CPU usage spikes, A.S.T.R.A automatically kills background bloatware and throttles non-essential apps to boost performance.
* **Project Glass (Advanced Security):** Utilizes Local Binary Patterns Histograms (LBPH) via OpenCV to scan and map your face. Automatically locks out intruders and secures the system the moment unauthorized access is detected.
* **Cinematic HUD:** A pixel-perfect, hardware-accelerated Tkinter dashboard providing real-time system telemetry, network speeds, and active protocol statuses in a highly detailed, futuristic layout.
* **Modular Architecture:** Built with an expandable plugin system, allowing seamless integration of IoT smart home controls, local LLM processing, and deep file indexing.

---

## 🛠️ Tech Stack

* **Language:** Python 3.14+
* **User Interface:** Tkinter (Canvas-based rendering)
* **Computer Vision:** OpenCV (`opencv-contrib-python`) & Haar Cascades
* **System Telemetry:** `psutil` (Kernel-level hardware tracking)
* **Data Storage:** SQLite, JSON, Pickle (Local Memory Banks)
* **Web Integrations (UI):** HTML5, CSS3, JavaScript (Three.js)

---

## 📁 Project Structure

```text
ASTRA_OS/
│
├── core/                   # Main initialization and brain logic
│   ├── ai_brain.py         # Neural routing and decision making
│   ├── logic_core.py       # Core execution threads
│   ├── main.py             # Primary boot sequence
│   └── astra_memory.db     # SQLite memory database
│
├── memory/                 # Stored encodings, audio, and whitelist data
│   ├── audio/              # Wake words and system sounds
│   ├── databases/          # Serialized pickle files for system access
│   ├── faces/              # Image data for Project Glass enrollment
│   └── memory_store/       # JSON and index files for fast retrieval
│
├── modules/                # Core operational protocols
│   ├── system/             # Hardware control, window management, and Initiative Protocol
│   ├── vision/             # Project Glass, Optics Engine, and Facial Training
│   └── voice/              # Offline STT/TTS and audio playback
│
├── plugins/                # Expandable agent capabilities
│   ├── ollama_engine.py    # Local LLM integration bridge
│   ├── system_agent.py     # Autonomous OS task execution
│   └── vector_db/          # Semantic search routing
│
├── security/               # Defense systems
│   ├── hardware_monitor.py # Kernel-level threat detection
│   └── sentry_mode.py      # Intrusion lockdown protocols
│
├── ui/                     # Visual assets and HUD scripts
│   ├── app_window.py       # Cinematic Tkinter Dashboard
│   ├── server.py           # Localhost server for web UI components
│   └── (HTML/JS/CSS assets)
│
├── astra_autoboot.bat      # Windows startup execution
├── requirements_mk2.txt    # Python dependencies
└── setup.py                # Environment configuration script

```

---

## ⚙️ Installation & Setup

**1. Clone the Repository**

```bash
git clone https://github.com/yourusername/ASTRA_OS.git
cd ASTRA_OS

```

**2. Create a Virtual Environment (Recommended)**

```bash
python -m venv astra_env
astra_env\Scripts\activate

```

**3. Install Dependencies**

```bash
pip install -r requirements_mk2.txt

```

*Note: Ensure you have a working webcam connected for the OpenCV face enrollment.*

**4. Run Project Glass Enrollment**
Before the system can secure your PC, you must register your biometrics as the Master User.

```bash
python modules/vision/train_faces.py

```

**5. Boot A.S.T.R.A**

```bash
python core/main.py

```

---

## 💻 Usage Instructions

* **HUD Controls:** Once A.S.T.R.A verifies your identity, the HUD will launch. Press `F11` to toggle Fullscreen mode. Press `ESC` to disengage the visual interface and return to windowed mode or close the dashboard.
* **Background Monitoring:** A.S.T.R.A runs silently in the background. If CPU or RAM hits critical thresholds (>85%), you will be notified audibly before the system autonomously clears bloatware.
* **Adding New Skills:** Developers can drop new Python scripts into the `plugins/` directory. The `system_agent.py` will automatically index and hook new capabilities into the main loop.

---

## 🛡️ License & Disclaimer

**Disclaimer:** The Initiative Protocol interacts directly with Windows process management. It is designed to terminate known bloatware. Please review the `whitelist.pickle` and `initiative.py` scripts to ensure your critical work applications are not flagged for termination during a heavy load event.

This project is licensed under the MIT License - see the LICENSE file for details.
