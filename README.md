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
git clone https://github.com/itsebasvz/redneuronalrgb.git
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

## Uso

Conectar la placa y ejecutar:
```bash
python recolectar_colores.py
```

Salida esperada:
```
✅ Conectado a /dev/ttyUSB0
Presiona:
    [l] → limon
    [p] → platano
    [f] → fondo
Ctrl+C para terminar.
```

Al presionar una tecla se registra la muestra; al terminar con Ctrl+C se guarda el CSV.

## Formato del CSV

Cada fila contiene:
```
timestamp | etiqueta | r | g | b
```
Ejemplo:
```
2025-11-11T20:31:55 | limon   | 1258 | 1684 | 746
2025-11-11T20:32:04 | platano | 1643 | 2156 | 932
```

## Estructura del proyecto
```
-redneuronalrgb/
-├── recolectar_colores.py
-├── .env
-├── .gitignore
-├── requirements.txt
-└── README.md
```

## Notas
- Ajusta `PUERTO` y `BAUDIOS` según tu placa.
- Añade/filtra etiquetas según las clases que necesites para entrenamiento.
