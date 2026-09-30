# Real-Time PPE Detection & Safety Compliance System

A local, real-time computer vision system built with **YOLOv11** and **OpenCV** to monitor Personal Protective Equipment (PPE) compliance in industrial environments.

It detects workers and safety gear (helmets, vests, goggles), evaluates individual compliance, triggers alerts, automatically captures timestamped evidence, and logs audit data for analytics.

---

## ✨ Key Features
* **100% Local & Edge Execution:** Runs on-site with live camera feeds, low latency, and zero cloud dependency.
* **Person-to-PPE Association:** Dynamically maps detected safety gear to individual worker bounding boxes.
* **Multi-Level Compliance:** Categorizes workers as **OK** (Full PPE), **PARTIAL** (Missing secondary gear), or **CRITICAL** (Missing helmet).
* **Industrial HMI & Alerts:** On-screen status overlays, visual warning banners, and configurable audible alarms.
* **Automated Evidence Logging:** Saves timestamped violation snapshots (`.jpg`) and updates an audit log (`evidencias_log.csv`) with adjustable cooldowns.
* **Analytics Module:** Includes `analizar_evidencias.py` to parse logs and generate graphical compliance reports.

---

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Core Libraries:** Ultralytics YOLOv11, PyTorch, OpenCV, Pandas, Matplotlib

---

## 🚀 Quick Start

1. **Install Dependencies:**
   pip install -r requirements.txt

2. **Run Live System:**
   python predict.py
   * **In-app Controls:** A (Toggle Audio Alarm) | C (Toggle Evidence Capture) | Q (Quit)

3. **Generate Analytics Report:**
   python analizar_evidencias.py

---

## 🔗 Resources
* **GitHub Repository:** [DCD55/sistema-deteccion-ppe](https://github.com/DCD55/sistema-deteccion-ppe)
* **Dataset:** [Construction PPE Dataset](https://github.com/ultralytics/assets/releases/download/v0.0.0/construction-ppe.zip)

## 🔗 Resources & External Links
* **GitHub Repository:** [DCD55/sistema-deteccion-ppe](https://github.com/DCD55/sistema-deteccion-ppe)
* **Project Files (Google Drive):** [Google Drive Folder](https://drive.google.com/drive/folders/1inbOkgP2bKxKCOdcVY17fXrVXQtNH95j?usp=drive_link)
* **Official Dataset (PPE):** [Construction PPE Dataset (ZIP)](https://github.com/ultralytics/assets/releases/download/v0.0.0/construction-ppe.zip)


GitHub: https://github.com/DCD55/sistema-deteccion-ppe

Google Drive: https://drive.google.com/drive/folders/1inbOkgP2bKxKCOdcVY17fXrVXQtNH95j?usp=drive_link

Base de Datos Oficial (EPP): https://github.com/ultralytics/assets/releases/download/v0.0.0/construction-ppe.zip
