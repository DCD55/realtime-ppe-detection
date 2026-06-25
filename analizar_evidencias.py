import os
import csv
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt

LOG_CSV = "evidencias_log.csv"
REPORT_DIR = "reportes"


def asegurar_directorio(ruta):
    os.makedirs(ruta, exist_ok=True)


def leer_eventos():
    """Lee el archivo CSV con las evidencias registradas."""
    if not os.path.exists(LOG_CSV):
        print(f"❌ No se encontró el archivo {LOG_CSV}. Corre el sistema primero.")
        return []

    eventos = []
    with open(LOG_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            eventos.append(row)

    return eventos


def analizar_eventos(eventos):
    """Analiza los eventos del CSV y genera estadísticas + gráficas."""
    if not eventos:
        print("No hay eventos para analizar.")
        return

    total_eventos = len(eventos)
    conteo_modo = Counter(e["ppe_mode"] for e in eventos)
    conteo_faltas_por_tipo = Counter()
    conteo_por_dia = Counter()

    # Procesar eventos
    for e in eventos:
        # Faltas agrupadas, ej: helmet1_vest2
        faltas_str = e["faltas_agrupadas"]
        if faltas_str and faltas_str != "falta_epp":
            partes = faltas_str.split("_")
            for p in partes:
                for tipo in ["helmet", "vest", "goggles"]:
                    if p.startswith(tipo):
                        num = p.replace(tipo, "")
                        num = int(num) if num.isdigit() else 1
                        conteo_faltas_por_tipo[tipo] += num

        # Eventos por día
        fecha = e["timestamp"].split(" ")[0]
        conteo_por_dia[fecha] += 1

    # === Resumen en consola ===
    print("\n=== RESUMEN DE EVENTOS DE FALTA EPP ===")
    print(f"Total de eventos registrados: {total_eventos}\n")

    print("Eventos por modo PPE:")
    for modo, cnt in conteo_modo.items():
        print(f"  - {modo}: {cnt}")

    print("\nFaltas acumuladas por tipo:")
    if conteo_faltas_por_tipo:
        for tipo, cnt in conteo_faltas_por_tipo.items():
            print(f"  - {tipo}: {cnt}")
    else:
        print("  (sin desglose por tipo aún)")

    print("\nEventos por día:")
    for dia, cnt in sorted(conteo_por_dia.items()):
        print(f"  - {dia}: {cnt}")

    # === Generar gráficas automáticas ===
    asegurar_directorio(REPORT_DIR)
    graficar_faltas_por_tipo(conteo_faltas_por_tipo)
    graficar_eventos_por_dia(conteo_por_dia)
    graficar_eventos_por_modo(conteo_modo)

    print("\n📊 Gráficas guardadas en carpeta 'reportes/'.")


# ======= GRAFICAS =======

def graficar_faltas_por_tipo(conteo):
    if not conteo:
        return

    etiquetas = list(conteo.keys())
    valores = [conteo[e] for e in etiquetas]

    plt.figure()
    plt.bar(etiquetas, valores, color=["red", "orange", "blue"])
    plt.title("Faltas acumuladas por tipo de EPP")
    plt.xlabel("Tipo de EPP")
    plt.ylabel("Cantidad de faltas")
    plt.tight_layout()

    ruta = os.path.join(REPORT_DIR, "faltas_por_tipo.png")
    plt.savefig(ruta)
    plt.close()


def graficar_eventos_por_dia(conteo_dia):
    if not conteo_dia:
        return

    dias = sorted(conteo_dia.keys())
    valores = [conteo_dia[d] for d in dias]

    plt.figure()
    plt.bar(dias, valores, color="purple")
    plt.title("Eventos de falta por día")
    plt.xlabel("Fecha")
    plt.ylabel("Cantidad de eventos")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    ruta = os.path.join(REPORT_DIR, "eventos_por_dia.png")
    plt.savefig(ruta)
    plt.close()


def graficar_eventos_por_modo(conteo_modo):
    if not conteo_modo:
        return

    modos = list(conteo_modo.keys())
    valores = [conteo_modo[m] for m in modos]

    plt.figure()
    plt.bar(modos, valores, color="green")
    plt.title("Eventos por modo PPE")
    plt.xlabel("Modo de protección")
    plt.ylabel("Cantidad de eventos")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()

    ruta = os.path.join(REPORT_DIR, "eventos_por_modo_ppe.png")
    plt.savefig(ruta)
    plt.close()


def main():
    print("=== ANALISIS DE EVIDENCIAS ===")
    eventos = leer_eventos()
    analizar_eventos(eventos)


if __name__ == "__main__":
    main()
