# 🧠 Recolector de Colores (TCS34725 + Python + CSV)

Una utilidad para leer valores RGB desde un sensor TCS34725 conectado a una placa (Arduino / ESP32) vía serial y guardar las muestras en un CSV para entrenar una red neuronal que clasifique colores o frutas (por ejemplo: limón 🍋, plátano 🍌).

## Requisitos

### Hardware
- Sensor TCS34725 conectado a una placa (Arduino o ESP32).
- Cable USB conectado al equipo.

### Software
- Python 3.9+.
- Git (opcional).

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tuusuario/redneuronalrgb.git
cd redneuronalrgb
```

2. Crear y activar un entorno virtual:

En Linux / macOS:
```bash
python -m venv venv
source venv/bin/activate
```

En Windows (CMD / PowerShell):
```bash
python -m venv venv
venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Configuración (.env)

Crear un archivo `.env` en la raíz con las variables:

Ejemplo (Linux/macOS):

▶️ Ejecución del programa

Conecta tu placa y ejecuta:
   python recolectar_colores.py

Salida esperada:
   ✅ Conectado a /dev/ttyUSB0
   Presiona:
     [l] → limon
     [p] → platano
     [f] → fondo
   Ctrl+C para terminar.

Al presionar una tecla, se registrará la muestra y al finalizar con Ctrl+C, se guardará el archivo CSV.

🧩 Estructura del CSV resultante

timestamp | etiqueta | r | g | b
-----------|-----------|---|---|---
2025-11-11T20:31:55 | limon | 1258 | 1684 | 746
2025-11-11T20:32:04 | platano | 1643 | 2156 | 932

🧰 Archivos del proyecto

redneuronalrgb/
├── recolectar_colores.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md