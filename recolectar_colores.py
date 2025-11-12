import serial
import csv
import os
import signal
import sys
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

PUERTO = os.getenv("SERIAL_PORT", "/dev/ttyUSB0")
BAUDIOS = int(os.getenv("BAUD_RATE", "115200"))
CSV_FILE = os.getenv("CSV_FILE", "datos_colores.csv")

# Lista donde se almacenarán los datos antes de guardar
datos = []

def guardar_csv():
    """Guarda los datos recolectados en un CSV ordenado."""
    if not datos:
        print("⚠️ No se registraron datos.")
        return
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "label", "R", "G", "B"])
        writer.writerows(datos)
    print(f"💾 Datos guardados en {CSV_FILE}")

def signal_handler(sig, frame):
    """Maneja Ctrl+C para guardar antes de salir."""
    print("\n🛑 Finalizando y guardando datos...")
    guardar_csv()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def parsear_raw(linea):
    """Extrae R, G y B de una línea RAW -> R:xxxx G:xxxx B:xxxx"""
    try:
        partes = linea.split()
        R = int(partes[2].split(":")[1])
        G = int(partes[3].split(":")[1])
        B = int(partes[4].split(":")[1])
        return R, G, B
    except Exception:
        return None

def main():
    print(f"✅ Conectado a {PUERTO}")
    print("Presiona:")
    print("  [l] → limon")
    print("  [p] → platano")
    print("  [f] → fondo")
    print("Ctrl+C para terminar.\n")

    ser = serial.Serial(PUERTO, BAUDIOS, timeout=1)

    ultima_linea = ""
    while True:
        try:
            linea = ser.readline().decode("utf-8", errors="ignore").strip()
            if not linea:
                continue

            # Si es una línea RAW, guardarla para usarla al presionar una tecla
            if linea.startswith("RAW ->"):
                ultima_linea = linea

            # Leer entrada del teclado (no bloqueante)
            import select, sys, termios
            dr, _, _ = select.select([sys.stdin], [], [], 0)
            if dr:
                tecla = sys.stdin.read(1).lower()
                if tecla in ["l", "p", "f"] and ultima_linea:
                    rgb = parsear_raw(ultima_linea)
                    if rgb:
                        etiqueta = {"l": "limon", "p": "platano", "f": "fondo"}[tecla]
                        timestamp = datetime.now().isoformat(timespec="seconds")
                        fila = [timestamp, etiqueta, *rgb]
                        datos.append(fila)
                        print(f"📸 Muestra registrada: {fila}")
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    main()
