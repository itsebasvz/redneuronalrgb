import serial
import os
import signal
import sys
from datetime import datetime
from dotenv import load_dotenv
import joblib
import numpy as np

# Cargar variables del .env
load_dotenv()

PUERTO = os.getenv("SERIAL_PORT", "/dev/ttyUSB0")
BAUDIOS = int(os.getenv("BAUD_RATE", "115200"))

# Cargar el modelo y el scaler entrenados
print("🧠 Cargando modelo de red neuronal...")
try:
    red_neuronal = joblib.load('modelo_red_neuronal.pkl')
    scaler = joblib.load('scaler.pkl')
    print("✅ Modelo cargado correctamente\n")
except FileNotFoundError:
    print("❌ Error: No se encontró el modelo entrenado.")
    print("   Por favor, ejecuta primero: python entrenar_red_neuronal.py")
    sys.exit(1)

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

def predecir_fruta(r, g, b):
    """
    Predice si los valores RGB corresponden a un limón o manzana.
    Retorna la predicción y las probabilidades.
    """
    # Normalizar los valores usando el mismo scaler del entrenamiento
    valores = scaler.transform([[r, g, b]])
    prediccion = red_neuronal.predict(valores)[0]
    probabilidades = red_neuronal.predict_proba(valores)[0]
    
    # Obtener las clases
    clases = red_neuronal.classes_
    
    return prediccion, probabilidades, clases

def signal_handler(sig, frame):
    """Maneja Ctrl+C para salir limpiamente."""
    print("\n🛑 Finalizando clasificación en vivo...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main():
    print("="*60)
    print("🍋🍎 CLASIFICADOR DE FRUTAS EN TIEMPO REAL")
    print("="*60)
    print(f"✅ Conectado a {PUERTO}")
    print("📡 Esperando datos del sensor TCS34725...")
    print("👉 Presiona ENTER para clasificar la fruta actual")
    print("Ctrl+C para terminar.\n")

    ser = serial.Serial(PUERTO, BAUDIOS, timeout=1)

    ultima_linea_raw = ""

    while True:
        try:
            linea = ser.readline().decode("utf-8", errors="ignore").strip()
            if not linea:
                continue

            # Si es una línea RAW, guardarla
            if linea.startswith("RAW ->"):
                ultima_linea_raw = linea

            # Leer entrada del teclado (no bloqueante)
            import select
            dr, _, _ = select.select([sys.stdin], [], [], 0)
            if dr:
                tecla = sys.stdin.read(1)
                if tecla == '\n' and ultima_linea_raw:  # Si presiona Enter
                    rgb = parsear_raw(ultima_linea_raw)
                    if rgb:
                        r, g, b = rgb
                        
                        # Hacer la predicción
                        prediccion, probabilidades, clases = predecir_fruta(r, g, b)
                        
                        # Verificar si la confianza es suficiente (umbral de 70%)
                        confianza_maxima = max(probabilidades)
                        
                        # Mostrar resultados
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        
                        if confianza_maxima < 0.70:  # Si la confianza es menor al 70%
                            print(f"\n[{timestamp}] RGB({r:4d}, {g:4d}, {b:4d}) → ❓ OBJETO NO RECONOCIDO")
                            print(f"   Confianza insuficiente (< 70%)")
                        else:
                            # Crear emoji según la predicción
                            emoji = "🍋" if prediccion == "limon" else "🍎"
                            print(f"\n[{timestamp}] RGB({r:4d}, {g:4d}, {b:4d}) → {emoji} {prediccion.upper()}")
                        
                        # Mostrar probabilidades
                        for i, clase in enumerate(clases):
                            barra = "█" * int(probabilidades[i] * 20)
                            print(f"   {clase:10s}: {probabilidades[i]:5.1%} {barra}")
                        print("\n👉 Presiona ENTER para clasificar otra vez...")

        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    main()
