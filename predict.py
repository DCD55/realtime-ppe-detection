# predict.py
# Sistema de detección de EPP (PPE) con YOLO + Webcam
# - Análisis por persona (P1, P2, ...)
# - Panel PPE compacto estilo HMI
# - Semáforo en el bounding box de la persona
# - Barra superior flotante con PERSONAS / EN REGLA / CON FALTA
# - Guardado de evidencias (CAP) solo cuando cambie el estado de faltas
# - Evidencias por día: evidencias/AAAA-MM-DD/...
# - Log en CSV de cada CAP: evidencias_log.csv
# - Menú para cooldown de CAP: 5, 15, 25 s
# - Modos de PPE: completo / solo casco / casco + chaleco
# - Alarma sonora SOLO si falta casco (status "bad"), cada 5 s
# - Alarma visual "ALERTA / SIN CASCO" en la esquina superior derecha
# - Teclas: 'a' (alarma ON/OFF), 'c' (CAP/evidencias ON/OFF), 'q' (salir)
# - Menú inferior horizontal: [Q] Exit | [A] Alarma | [C] Cap

from ultralytics import YOLO
import glob
import os
import cv2
import time
import csv
from datetime import datetime

# Intentar importar winsound para Windows (beep)
try:
    import winsound
    WINDOWS = True
except ImportError:
    WINDOWS = False

# PPE disponibles
ALL_PPE = ["vest", "helmet", "goggles"]

# Carpeta base para evidencias
EVIDENCE_DIR = "evidencias"
os.makedirs(EVIDENCE_DIR, exist_ok=True)

# Archivo CSV para log de eventos
LOG_CSV = "evidencias_log.csv"


def init_log_csv():
    """Crea el archivo CSV de log si no existe, con encabezados."""
    if not os.path.exists(LOG_CSV):
        with open(LOG_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp",
                "ppe_mode",
                "total_personas",
                "personas_ok",
                "personas_con_falta",
                "faltas_agrupadas",
                "ruta_cap"
            ])


def log_event(ppe_mode_name, total_personas, personas_ok, personas_con_falta, faltas_agrupadas, ruta_cap):
    """Escribe una fila en el CSV de eventos de CAP."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_CSV, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp,
            ppe_mode_name,
            total_personas,
            personas_ok,
            personas_con_falta,
            faltas_agrupadas,
            ruta_cap
        ])


def predict_images(model):
    """Predicción sobre imágenes del dataset de prueba."""
    test_images = glob.glob("datasets/construction-ppe/images/test/*")
    print(f"Procesando {len(test_images)} imágenes de ejemplo:")
    for img in test_images:
        print(f"  - {os.path.basename(img)}")

    _ = model.predict(source=test_images, save=True, conf=0.25)
    print("\nProcesadas exitosamente. Guardadas en 'runs/detect/'.")


def draw_mini_menu(frame, sound_enabled, evidence_enabled):
    """
    Menú horizontal inferior:
    [Q] Exit | [A] Alarma | [C] Cap
    Con colores: verde ON, rojo OFF.
    """
    h, w, _ = frame.shape

    panel_h = 35
    y1 = h - panel_h - 10
    y2 = h - 10
    x1 = 10
    x2 = w - 10

    # Fondo semitransparente horizontal
    overlay = frame.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 0), -1)
    frame = cv2.addWeighted(overlay, 0.50, frame, 0.50, 0)

    font = cv2.FONT_HERSHEY_SIMPLEX
    base_y = y1 + 23

    white = (255, 255, 255)
    alarm_color = (0, 255, 0) if sound_enabled else (0, 0, 255)
    evid_color = (0, 255, 0) if evidence_enabled else (0, 0, 255)

    text_exit = "[Q] Exit"
    text_alarm = "[A] Alarma"
    text_evid = "[C] Cap"

    spacing = 250  # separación horizontal

    # EXIT
    cv2.putText(frame, text_exit, (x1 + 15, base_y),
                font, 0.6, white, 2)

    # ALARMA
    cv2.putText(frame, text_alarm, (x1 + 15 + spacing, base_y),
                font, 0.6, alarm_color, 2)

    # CAP
    cv2.putText(frame, text_evid, (x1 + 15 + spacing * 2, base_y),
                font, 0.6, evid_color, 2)

    return frame


def seleccionar_modo_ppe():
    """
    Menú para seleccionar el modo de PPE:
      1 - Casco + chaleco + goggles
      2 - Solo casco
      3 - Casco + chaleco
    """
    print("\n=== MODO PPE REQUERIDO ===")
    print("1 - Casco + Chaleco + Goggles")
    print("2 - Solo Casco")
    print("3 - Casco + Chaleco")

    op = input("Opción: ").strip()

    if op == "1":
        required = ["helmet", "vest", "goggles"]
        name = "Casco+Chaleco+Goggles"
    elif op == "2":
        required = ["helmet"]
        name = "Solo Casco"
    elif op == "3":
        required = ["helmet", "vest"]
        name = "Casco+Chaleco"
    else:
        print("Opción no válida, se usará Casco+Chaleco+Goggles por defecto.")
        required = ["helmet", "vest", "goggles"]
        name = "Casco+Chaleco+Goggles"

    print(f"➡ Modo PPE seleccionado: {name}")
    return required, name


def predict_webcam(model, CAPTURE_COOLDOWN, required_ppe, ppe_mode_name):
    """
    Predicción en tiempo real desde la webcam con:
    - Panel PPE por persona (compacto)
    - Semáforo de cumplimiento
    - Barra superior flotante de resumen
    - Evidencias con cooldown y solo cuando cambie el estado
    - Alarmas visual y sonora
    - Menú de teclas inferior
    """
    print("=== INICIANDO WEBCAM ===")
    print("Clases detectadas:", model.names)
    print(f"📸 Cooldown mínima entre CAP: {CAPTURE_COOLDOWN} s")
    print(f"🦺 Modo PPE requerido: {ppe_mode_name}")
    print("🔊 Alarma sonora: cada 5 s SOLO si falta casco (status 'bad')")
    print("🎛️ Controles: 'a' = alarma ON/OFF, 'c' = CAP ON/OFF, 'q' = salir")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error al acceder a la cámara.")
        return

    last_capture_time = 0.0
    last_beep_time = 0.0
    ALARM_COOLDOWN = 5.0  # segundos entre beeps

    sound_enabled = True       # alarma sonora activa
    evidence_enabled = True    # guardado de evidencias activo

    # Para CAP solo cuando cambie el estado
    previous_fault_signature = None

    while True:
        ok, frame = cap.read()
        if not ok:
            print("No se pudo leer frame.")
            break

        annotated = frame.copy()
        result = model.predict(frame, conf=0.25, verbose=False)[0]
        boxes = result.boxes

        # Si no hay detecciones, solo mostramos cámara + mini menú + teclas
        if boxes is None or boxes.cls is None:
            annotated = draw_mini_menu(annotated, sound_enabled, evidence_enabled)
            cv2.imshow("Detección PPE", annotated)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break
            elif key == ord("a"):
                sound_enabled = not sound_enabled
                estado = "ACTIVADA" if sound_enabled else "DESACTIVADA"
                print(f"🔊 Alarma sonora {estado}")
            elif key == ord("c"):
                evidence_enabled = not evidence_enabled
                estado = "ACTIVADO" if evidence_enabled else "DESACTIVADO"
                print(f"📸 CAP (evidencias) {estado}")
            continue

        h, w, _ = annotated.shape
        persons = []
        ppe_items = []

        xyxy = boxes.xyxy.tolist()
        cls_ids = boxes.cls.int().tolist()

        # Clasificar detecciones en personas y EPP
        for bbox, cid in zip(xyxy, cls_ids):
            cname = model.names[int(cid)]
            if cname.lower() == "person":
                persons.append({"bbox": bbox, "ppe": set()})
            elif cname in ALL_PPE:
                ppe_items.append({"bbox": bbox, "type": cname})

        # Dibujar cajas de EPP (sin labels, solo color por tipo)
        for item in ppe_items:
            x1, y1, x2, y2 = map(int, item["bbox"])
            if item["type"] == "helmet":
                color = (255, 0, 0)
            elif item["type"] == "goggles":
                color = (0, 255, 255)
            elif item["type"] == "vest":
                color = (0, 165, 255)
            else:
                color = (255, 255, 255)

            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)

        # Asignar PPE a personas (centro del EPP dentro del bbox de persona)
        for ppe in ppe_items:
            x1, y1, x2, y2 = ppe["bbox"]
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

            for person in persons:
                px1, py1, px2, py2 = person["bbox"]
                if px1 <= cx <= px2 and py1 <= cy <= py2:
                    person["ppe"].add(ppe["type"])
                    break

        # Evaluar estado por persona
        total_personas = len(persons)
        personas_ok = 0

        for person in persons:
            has_required = all(e in person["ppe"] for e in required_ppe)
            # Para severidad usamos el casco como referencia
            has_helmet = "helmet" in person["ppe"]

            if has_required:
                status = "ok"
                personas_ok += 1
            elif has_helmet:
                status = "partial"
            else:
                status = "bad"  # sin casco (si el casco es requerido) → falta grave

            person["status"] = status

        personas_con_falta = total_personas - personas_ok

        # === BARRA SUPERIOR COMPACTA, FLOTANTE Y CON BORDES REDONDEADOS ===
        texto = f"PERSONAS: {total_personas} | EN REGLA: {personas_ok} | CON FALTA: {personas_con_falta}"

        font_top = cv2.FONT_HERSHEY_SIMPLEX
        font_scale_top = 0.55
        thick_top = 2

        (text_w, text_h) = cv2.getTextSize(texto, font_top, font_scale_top, thick_top)[0]

        bar_h = 28
        pad_x = 12
        pad_y = 8
        radius = 10

        x1_bar = pad_x
        y1_bar = pad_y
        x2_bar = w - pad_x
        y2_bar = pad_y + bar_h

        overlay_bar = annotated.copy()

        # Fondo negro con bordes redondeados
        cv2.rectangle(overlay_bar, (x1_bar + radius, y1_bar), (x2_bar - radius, y2_bar), (0, 0, 0), -1)
        cv2.rectangle(overlay_bar, (x1_bar, y1_bar + radius), (x2_bar, y2_bar - radius), (0, 0, 0), -1)
        cv2.circle(overlay_bar, (x1_bar + radius, y1_bar + radius), radius, (0, 0, 0), -1)
        cv2.circle(overlay_bar, (x2_bar - radius, y1_bar + radius), radius, (0, 0, 0), -1)
        cv2.circle(overlay_bar, (x1_bar + radius, y2_bar - radius), radius, (0, 0, 0), -1)
        cv2.circle(overlay_bar, (x2_bar - radius, y2_bar - radius), radius, (0, 0, 0), -1)

        annotated = cv2.addWeighted(overlay_bar, 0.55, annotated, 0.45, 0)

        # Texto centrado
        text_x = (w - text_w) // 2
        text_y = y1_bar + bar_h - 7

        cv2.putText(
            annotated,
            texto,
            (text_x, text_y),
            font_top,
            font_scale_top,
            (255, 255, 255),
            thick_top,
        )

        # === Dibujar cajas de personas + panel PPE compacto ===
        for idx, person in enumerate(persons):
            x1p, y1p, x2p, y2p = map(int, person["bbox"])

            # Color de caja según status
            if person["status"] == "ok":
                color_box = (0, 255, 0)
            elif person["status"] == "partial":
                color_box = (0, 255, 255)
            else:
                color_box = (0, 0, 255)

            cv2.rectangle(annotated, (x1p, y1p), (x2p, y2p), color_box, 3)

            # ------- PANEL PPE COMPACTO (estilo HMI) -------
            vest_ok = "OK" if "vest" in person["ppe"] else "X"
            helm_ok = "OK" if "helmet" in person["ppe"] else "X"
            gogg_ok = "OK" if "goggles" in person["ppe"] else "X"

            lines = [
                f"P{idx+1}  PPE",
                f"VEST   {vest_ok}",
                f"HELM   {helm_ok}",
                f"GOGG   {gogg_ok}",
            ]

            font_panel = cv2.FONT_HERSHEY_SIMPLEX
            scale_panel = 0.45
            thick_panel = 1

            widths = [cv2.getTextSize(t, font_panel, scale_panel, thick_panel)[0][0] for t in lines]
            panel_w = max(widths) + 12
            panel_h = 18 + 3 * 16 + 8  # header + 3 líneas + margen

            # Ubicar en la esquina inferior izquierda del bbox
            px1 = max(0, min(x1p, w - panel_w - 1))
            py1 = max(0, min(y2p - panel_h, h - panel_h - 1))
            px2, py2 = px1 + panel_w, py1 + panel_h

            # Fondo semitransparente
            overlay_p = annotated.copy()
            cv2.rectangle(overlay_p, (px1, py1), (px2, py2), (0, 0, 0), -1)
            annotated = cv2.addWeighted(overlay_p, 0.65, annotated, 0.35, 0)

            # Header naranja delgado
            header_h = 18
            cv2.rectangle(annotated, (px1, py1), (px2, py1 + header_h), (0, 140, 255), -1)

            # Borde gris
            cv2.rectangle(annotated, (px1, py1), (px2, py2), (90, 90, 90), 1)

            # Texto header
            cv2.putText(
                annotated,
                lines[0],
                (px1 + 6, py1 + header_h - 4),
                font_panel,
                scale_panel,
                (0, 0, 0),
                1,
            )

            # Líneas VEST / HELM / GOGG
            base_y = py1 + header_h + 14
            for i, label in enumerate(["VEST", "HELM", "GOGG"]):
                if label == "VEST":
                    status_txt = vest_ok
                elif label == "HELM":
                    status_txt = helm_ok
                else:
                    status_txt = gogg_ok

                if status_txt == "OK":
                    col = (0, 255, 0)
                else:
                    col = (0, 255, 255)

                # Etiqueta (blanco)
                cv2.putText(
                    annotated,
                    label,
                    (px1 + 6, base_y + i * 16),
                    font_panel,
                    scale_panel,
                    (255, 255, 255),
                    1,
                )
                # Estado (color)
                cv2.putText(
                    annotated,
                    status_txt,
                    (px1 + 6 + 60, base_y + i * 16),
                    font_panel,
                    scale_panel,
                    col,
                    1,
                )
            # ------- FIN PANEL PPE -------

        # === Listas de faltas ===
        personas_sin_casco = [p for p in persons if p["status"] == "bad"]      # sin casco
        personas_con_falta_lista = [p for p in persons if p["status"] != "ok"]  # cualquier falta

        # === Alarma visual pequeña (esquina superior derecha) si falta casco ===
        if personas_sin_casco:
            box_w, box_h = 150, 40
            ax2 = w - 10
            ax1 = ax2 - box_w
            ay1 = 55          # más abajo para no tapar la barra
            ay2 = ay1 + box_h

            overlay_alert = annotated.copy()
            cv2.rectangle(overlay_alert, (ax1, ay1), (ax2, ay2), (0, 0, 255), -1)
            annotated = cv2.addWeighted(overlay_alert, 0.6, annotated, 0.4, 0)

            cv2.putText(
                annotated,
                "ALERTA",
                (ax1 + 20, ay1 + 17),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2,
            )
            cv2.putText(
                annotated,
                "SIN CASCO",
                (ax1 + 12, ay1 + 34),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (255, 255, 255),
                1,
            )

        # === Alarma sonora: SOLO sin casco, cada 5 s, si está activada ===
        if personas_sin_casco and sound_enabled:
            now = time.time()
            if now - last_beep_time >= ALARM_COOLDOWN:
                if WINDOWS:
                    winsound.Beep(1200, 300)
                else:
                    print("\a")
                last_beep_time = now

        # === CAP / Evidencias: solo cuando cambie el estado, con cooldown ===
        # Construimos una "firma" de faltas globales para comparar con el frame anterior
        if personas_con_falta_lista and evidence_enabled:
            # Contar faltas de cada tipo de PPE requerido
            faltas_globales = {}
            for p in personas_con_falta_lista:
                for e in required_ppe:
                    if e not in p["ppe"]:
                        faltas_globales[e] = faltas_globales.get(e, 0) + 1

            # Convertimos la firma a algo comparable (tupla ordenada)
            firma_actual = (
                personas_con_falta,
                tuple(sorted(faltas_globales.items()))
            )

            now = time.time()
            # Solo guardar CAP si hay cambio de firma y pasó el cooldown
            if firma_actual != previous_fault_signature and (now - last_capture_time >= CAPTURE_COOLDOWN):
                # Carpeta por día
                today_str = datetime.now().strftime("%Y-%m-%d")
                day_dir = os.path.join(EVIDENCE_DIR, today_str)
                os.makedirs(day_dir, exist_ok=True)

                faltas_str = "_".join([f"{k}{v}" for k, v in faltas_globales.items()]) if faltas_globales else "falta_epp"

                timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp_str}_faltas_{faltas_str}.jpg"
                filepath = os.path.join(day_dir, filename)

                cv2.imwrite(filepath, annotated)
                print(f"📸 CAP guardada: {filepath}")

                # Log en CSV
                log_event(
                    ppe_mode_name=ppe_mode_name,
                    total_personas=total_personas,
                    personas_ok=personas_ok,
                    personas_con_falta=personas_con_falta,
                    faltas_agrupadas=faltas_str,
                    ruta_cap=filepath
                )

                last_capture_time = now
                previous_fault_signature = firma_actual
        elif not personas_con_falta_lista:
            # Si ya no hay faltas, reseteamos la firma para detectar la siguiente
            previous_fault_signature = None

        # === Mini menú en pantalla (abajo, horizontal) ===
        annotated = draw_mini_menu(annotated, sound_enabled, evidence_enabled)

        # === Mostrar frame y leer teclado ===
        cv2.imshow("Detección PPE", annotated)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        elif key == ord("a"):
            sound_enabled = not sound_enabled
            estado = "ACTIVADA" if sound_enabled else "DESACTIVADA"
            print(f"🔊 Alarma sonora {estado}")
        elif key == ord("c"):
            evidence_enabled = not evidence_enabled
            estado = "ACTIVADO" if evidence_enabled else "DESACTIVADO"
            print(f"📸 CAP (evidencias) {estado}")

    cap.release()
    cv2.destroyAllWindows()


def seleccionar_cooldown():
    """Menú de configuración para el cooldown de CAP."""
    print("\n=== CONFIGURACIÓN DE CAP (EVIDENCIAS) ===")
    print("Tiempo mínimo entre CAP (cuando cambie el estado):")
    print("1 - 5 segundos")
    print("2 - 15 segundos")
    print("3 - 25 segundos")

    op = input("Opción: ").strip()
    if op == "1":
        return 5
    elif op == "2":
        return 15
    elif op == "3":
        return 25
    else:
        print("Opción no válida, usando 5 segundos por defecto.")
        return 5


def main():
    print("=== PREDICT.PY INICIADO ===")

    # Inicializar archivo de log si no existe
    init_log_csv()

    model = YOLO("runs/detect/train/yolo11n-construction-ppe/weights/best.pt")

    print("\nModo de predicción:")
    print("1 - Imágenes de prueba")
    print("2 - Webcam en tiempo real")

    opcion = input("Opción: ").strip()

    if opcion == "1":
        predict_images(model)
    elif opcion == "2":
        required_ppe, ppe_mode_name = seleccionar_modo_ppe()
        cooldown = seleccionar_cooldown()
        predict_webcam(model, cooldown, required_ppe, ppe_mode_name)
    else:
        print("❌ Opción no válida.")


if __name__ == "__main__":
    main()
