import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Cargar datos del CSV
print("📂 Cargando datos desde datos_colores.csv...")
df = pd.read_csv('datos_colores.csv')

# Filtrar solo limones y manzanas (excluir fondo si existe)
df_filtrado = df[df['label'].isin(['limon', 'manzana'])]
print(f"✅ Datos cargados: {len(df_filtrado)} muestras")
print(f"   - Limones: {len(df_filtrado[df_filtrado['label'] == 'limon'])}")
print(f"   - Manzanas: {len(df_filtrado[df_filtrado['label'] == 'manzana'])}")

# Preparar características (X) y etiquetas (y)
X = df_filtrado[['R', 'G', 'B']].values
y = df_filtrado['label'].values

# Normalizar los datos (importante para redes neuronales)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Dividir en conjunto de entrenamiento y prueba (80% entrenamiento, 20% prueba)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n📊 División de datos:")
print(f"   - Entrenamiento: {len(X_train)} muestras")
print(f"   - Prueba: {len(X_test)} muestras")

# Crear red neuronal con una sola capa oculta
print("\n🧠 Entrenando red neuronal...")
red_neuronal = MLPClassifier(
    hidden_layer_sizes=(10,),  # Una sola capa con 10 neuronas
    activation='relu',          # Función de activación ReLU
    solver='adam',              # Optimizador Adam
    max_iter=1000,              # Número máximo de iteraciones
    random_state=42,
    verbose=True                # Mostrar progreso del entrenamiento
)

red_neuronal.fit(X_train, y_train)

# Hacer predicciones
y_pred_train = red_neuronal.predict(X_train)
y_pred_test = red_neuronal.predict(X_test)

# Evaluar el modelo
accuracy_train = accuracy_score(y_train, y_pred_train)
accuracy_test = accuracy_score(y_test, y_pred_test)

print("\n" + "="*50)
print("📈 RESULTADOS DEL MODELO")
print("="*50)
print(f"Precisión en entrenamiento: {accuracy_train*100:.2f}%")
print(f"Precisión en prueba: {accuracy_test*100:.2f}%")

print("\n📊 Reporte de clasificación (conjunto de prueba):")
print(classification_report(y_test, y_pred_test))

print("\n🔢 Matriz de confusión:")
print(confusion_matrix(y_test, y_pred_test))
print("   Filas: valores reales | Columnas: predicciones")

# Visualizar la frontera de decisión en 3D (espacio RGB)
print("\n🎨 Generando visualización 3D...")

fig = plt.figure(figsize=(15, 5))

# Subplot 1: Datos reales en espacio RGB
ax1 = fig.add_subplot(131, projection='3d')
limones = df_filtrado[df_filtrado['label'] == 'limon']
manzanas = df_filtrado[df_filtrado['label'] == 'manzana']

ax1.scatter(limones['R'], limones['G'], limones['B'], 
           c='yellow', marker='o', s=50, label='Limón 🍋', edgecolors='black', alpha=0.7)
ax1.scatter(manzanas['R'], manzanas['G'], manzanas['B'], 
           c='red', marker='^', s=50, label='Manzana 🍎', edgecolors='black', alpha=0.7)
ax1.set_xlabel('R (Rojo)')
ax1.set_ylabel('G (Verde)')
ax1.set_zlabel('B (Azul)')
ax1.set_title('Datos Reales en Espacio RGB')
ax1.legend()

# Subplot 2: Proyección 2D (R vs G)
ax2 = fig.add_subplot(132)
ax2.scatter(limones['R'], limones['G'], 
           c='yellow', marker='o', s=50, label='Limón 🍋', edgecolors='black', alpha=0.7)
ax2.scatter(manzanas['R'], manzanas['G'], 
           c='red', marker='^', s=50, label='Manzana 🍎', edgecolors='black', alpha=0.7)
ax2.set_xlabel('R (Rojo)')
ax2.set_ylabel('G (Verde)')
ax2.set_title('Proyección 2D: Rojo vs Verde')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Subplot 3: Proyección 2D (G vs B)
ax3 = fig.add_subplot(133)
ax3.scatter(limones['G'], limones['B'], 
           c='yellow', marker='o', s=50, label='Limón 🍋', edgecolors='black', alpha=0.7)
ax3.scatter(manzanas['G'], manzanas['B'], 
           c='red', marker='^', s=50, label='Manzana 🍎', edgecolors='black', alpha=0.7)
ax3.set_xlabel('G (Verde)')
ax3.set_ylabel('B (Azul)')
ax3.set_title('Proyección 2D: Verde vs Azul')
ax3.legend()
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('visualizacion_clasificacion.png', dpi=300, bbox_inches='tight')
print("✅ Visualización guardada en: visualizacion_clasificacion.png")

# Guardar el modelo entrenado
import joblib
joblib.dump(red_neuronal, 'modelo_red_neuronal.pkl')
joblib.dump(scaler, 'scaler.pkl')
print("\n💾 Modelo guardado en: modelo_red_neuronal.pkl")
print("💾 Scaler guardado en: scaler.pkl")

# Función para hacer predicciones nuevas
def predecir_fruta(r, g, b):
    """
    Predice si los valores RGB corresponden a un limón o manzana.
    """
    # Normalizar los valores
    valores = scaler.transform([[r, g, b]])
    prediccion = red_neuronal.predict(valores)[0]
    probabilidades = red_neuronal.predict_proba(valores)[0]
    
    return prediccion, probabilidades

# Ejemplo de uso
print("\n" + "="*50)
print("🔮 EJEMPLO DE PREDICCIÓN")
print("="*50)
ejemplo_limon = [1000, 1400, 650]  # Valores típicos de un limón
ejemplo_manzana = [1500, 900, 700]  # Valores típicos de una manzana

pred_limon, prob_limon = predecir_fruta(*ejemplo_limon)
pred_manzana, prob_manzana = predecir_fruta(*ejemplo_manzana)

print(f"\n🍋 RGB {ejemplo_limon} → Predicción: {pred_limon}")
print(f"   Probabilidades: Limón={prob_limon[0]:.2%}, Manzana={prob_limon[1]:.2%}")

print(f"\n🍎 RGB {ejemplo_manzana} → Predicción: {pred_manzana}")
print(f"   Probabilidades: Limón={prob_manzana[0]:.2%}, Manzana={prob_manzana[1]:.2%}")

print("\n✅ ¡Entrenamiento completado con éxito!")
