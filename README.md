# Personal Protective Equipment (PPE) Detection & Compliance Monitoring System

## Overview
This project is an end-to-end, locally deployed automated visual monitoring and safety compliance management system. Powered by computer vision and deep learning, it provides **real-time, live-stream** Personal Protective Equipment (PPE) detection (helmets, safety vests, etc.) in industrial and construction environments.

Designed to run **100% locally on-site with live camera feeds**, the system ensures ultra-low-latency processing, enhanced data privacy, and reliable offline operation without cloud dependency or internet lag.

Beyond live detection, the system tracks individual worker compliance, triggers instant security alerts upon safety violations, automatically **saves high-resolution screenshots as visual evidence of infractions**, records detection logs into a local database, and generates analytics reports with interactive charts to evaluate safety metrics over time.

## ✨ Key Features
* **Local & Edge Execution:** Runs entirely on local hardware for maximum data privacy, zero cloud dependency, and offline capability.
* **Live Feed & Real-Time Detection:** Processes live camera streams with instant inference to identify missing or compliant safety gear (helmets, vests, etc.).
* **Automatic Evidence Capture:** Automatically captures and stores timestamped screenshots/snapshots whenever a safety violation occurs.
* **Compliance & User Verification:** Checks whether specific users/workers meet mandatory safety requirements in real time.
* **Instant Automated Alerts:** Triggers immediate visual/audible local alerts whenever a safety violation is detected on live feeds.
* **Database Integration & Logging:** Stores structured detection records, timestamps, visual evidence file paths, user compliance statuses, and violation history locally for auditability.
* **Data Analytics & Visualization:** Processes stored compliance data (`analizar_evidencias.py`) to generate informative graphs and performance reports.

## 🚀 Technologies Used
* **Language:** Python
* **Computer Vision Model:** YOLO (You Only Look Once)
* **Frameworks & Libraries:** OpenCV, PyTorch, Matplotlib / Seaborn (Data Visualization), Pandas / NumPy
* **Hardware Acceleration:** CUDA (Local GPU support)
* **Database:** SQLite / Local Database Engine

## 📂 Repository Structure
* `train.py`: Script for training and fine-tuning the YOLO detection model locally.
* `predict.py`: Main execution script for local, live video/webcam stream inference, real-time alert triggering, and visual evidence screenshot saving.
* `analizar_evidencias.py`: Processing and analytics module that compiles local detection databases, links evidence screenshots, evaluates compliance rates, and generates graphical reports.
* `data.yaml`: Dataset configuration file defining training paths and PPE class labels.
* `requirements.txt`: Environment dependencies required to run the project locally.

## 📊 Workflow
1. **Live Camera Feed Capture:** Real-time stream processing from locally connected webcams or RTSP IP cameras.
2. **On-Premise Detection & Verification:** Edge-deployed YOLO model evaluates live video frames to verify PPE compliance for detected personnel.
3. **Instant Alerts, Evidence Capture & Logging:** Non-compliant events trigger immediate local warnings, automatically save a timestamped screenshot image as evidence, and register an entry into the local database.
4. **Reporting & Analytics:** `analizar_evidencias.py` aggregates historical logs and evidence files to produce visual graphs and safety compliance metrics.

## 🔗 Resources & External Links
* **GitHub Repository:** [DCD55/sistema-deteccion-ppe](https://github.com/DCD55/sistema-deteccion-ppe)
* **Project Files (Google Drive):** [Google Drive Folder](https://drive.google.com/drive/folders/1inbOkgP2bKxKCOdcVY17fXrVXQtNH95j?usp=drive_link)
* **Official Dataset (PPE):** [Construction PPE Dataset (ZIP)](https://github.com/ultralytics/assets/releases/download/v0.0.0/construction-ppe.zip)


GitHub: https://github.com/DCD55/sistema-deteccion-ppe

Google Drive: https://drive.google.com/drive/folders/1inbOkgP2bKxKCOdcVY17fXrVXQtNH95j?usp=drive_link

Base de Datos Oficial (EPP): https://github.com/ultralytics/assets/releases/download/v0.0.0/construction-ppe.zip
