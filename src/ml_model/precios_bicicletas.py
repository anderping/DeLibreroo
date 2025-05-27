import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pickle
import numpy as np

# Dataset de ejemplo ampliado (20 filas)
data = {
    'gear_count': [7, 10, 12, 21, 18, 24, 30, 8, 9, 15, 11, 20, 22, 16, 14, 25, 28, 19, 13, 17],
    'weight_kg': [10.5, 9.8, 8.9, 7.5, 8.0, 7.2, 6.8, 9.9, 10.1, 8.3, 9.0, 7.7, 7.3, 8.5, 9.2, 7.1, 6.9, 7.8, 8.7, 8.2],
    'frame_material': [0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1],  # 0=aluminio, 1=carbono
    'price_usd': [300, 450, 600, 700, 650, 800, 900, 320, 310, 560, 470, 680, 720, 590, 430, 810, 880, 670, 520, 600]
}

df = pd.DataFrame(data)

# Variables predictoras
X = df[['gear_count', 'weight_kg', 'frame_material']]

# Variable objetivo
y = df['price_usd']

# División en entrenamiento y test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar modelo regresión lineal
model = LinearRegression()
model.fit(X_train, y_train)

# Probar modelo con test
y_pred = model.predict(X_test)
print("Predicciones de prueba:", y_pred)

# Guardar modelo a disco
with open('modelo_precio_bicicletas.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Modelo guardado en 'modelo_precio_bicicletas.pkl'")
