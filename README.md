# Personal Protective Equipment (PPE) Detection & Compliance Monitoring System

## Overview
This project is an end-to-end automated visual monitoring and safety compliance management system. Powered by computer vision and deep learning, it provides real-time Personal Protective Equipment (PPE) detection (helmets, safety vests, etc.) in industrial and construction environments[span_0](start_span)[span_0](end_span).

Beyond basic detection, the system tracks individual worker compliance, triggers real-time security alerts upon safety violations, records detection logs into a structured database, and generates analytics reports with interactive charts to evaluate safety metrics over time.

## ✨ Key Features
* **Real-time PPE Detection:** Identifies compliance or missing safety gear (e.g., helmets, vests, safety glasses) using high-speed object detection models.
* **Compliance & User Verification:** Checks whether specific users/workers meet mandatory safety requirements before or during operations.
* **Automated Alerting System:** Generates instant alerts and visual logs whenever a safety violation or missing PPE is detected.
* **Database Integration & Logging:** Stores structured detection records, timestamps, user compliance statuses, and violation history for auditability.
* **Data Analytics & Visualization:** Processes stored compliance data (`analizar_evidencias.py`) to generate informative graphs and performance reports.

## 🚀 Technologies Used
* **Language:** Python
* **Computer Vision Model:** YOLO (You Only Look Once)
* **Frameworks & Libraries:** OpenCV, PyTorch, Matplotlib / Seaborn (Data Visualization), Pandas / NumPy
* **Hardware Acceleration:** CUDA (GPU support)
* **Database:** SQLite / MySQL / PostgreSQL (or file-based logging system)

## 📂 Repository Structure
* `train.py`: Script for training and fine-tuning the YOLO detection model.
* `predict.py`: Main execution script for real-time video/camera stream inference and live alert triggering.
* `analizar_evidencias.py`: Processing and analytics module that compiles detection databases, evaluates compliance rates, and generates graphical reports.
* `data.yaml`: Dataset configuration file defining training paths and PPE class labels.
* `requirements.txt`: Environment dependencies required to run the project.

## 📊 Workflow
1. **Video Feed Capture:** Real-time stream processing from cameras.
2. **Detection & Verification:** YOLO checks for missing or correctly worn PPE on detected personnel.
3. **Alerts & Logging:** Non-compliant instances trigger immediate alerts and register entry into the database.
4. **Reporting:** `analizar_evidencias.py` aggregates historical logs and produces visual charts and compliance metrics.

## 🔗 Resources & External Links
* **GitHub Repository:** [DCD55/sistema-deteccion-ppe](https://github.com/DCD55/sistema-deteccion-ppe)
* **Project Files (Google Drive):** [Google Drive Folder](https://drive.google.com/drive/folders/1inbOkgP2bKxKCOdcVY17fXrVXQtNH95j?usp=drive_link)
* **Official Dataset (PPE):** [Construction PPE Dataset (ZIP)](https://github.com/ultralytics/assets/releases/download/v0.0.0/construction-ppe.zip)

GitHub: https://github.com/DCD55/sistema-deteccion-ppe

Google Drive: https://drive.google.com/drive/folders/1inbOkgP2bKxKCOdcVY17fXrVXQtNH95j?usp=drive_link

Base de Datos Oficial (EPP): https://github.com/ultralytics/assets/releases/download/v0.0.0/construction-ppe.zip
