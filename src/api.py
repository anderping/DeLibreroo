# from sklearn.model_selection import train_test_split, cross_val_score
# from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
# from sklearn.linear_model import Lasso

import os
from flask import Flask, request, render_template, jsonify
import pickle
import numpy as np

os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.config["DEBUG"] = True

# Carga del modelo de bicicletas (regresión lineal)
model_bike = pickle.load(open("modelo_precio_bicicletas.pkl", "rb"))

# Puedes mantener tu DataFrame de libros y endpoints existentes si quieres

@app.route('/', methods=['GET'])
def home():
    return "<h1>DeLibreroo</h1><p>Esta es una API para predecir precios de bicicletas a manos de nuestro pedaleador lector IbAI, entrenado por el maestro MiguelAI.</p>"

# Endpoint para predecir precio bicicleta
@app.route('/predict', methods=['GET', 'POST'])
def predict_price_bike():
    # Obtener parámetros desde POST o GET
    try:
        if request.method == 'POST':
            gear_count = int(request.form.get('gear_count'))
            weight_kg = float(request.form.get('weight_kg'))
            frame_material = int(request.form.get('frame_material'))
        else:  # GET
            gear_count = int(request.args.get('gear_count'))
            weight_kg = float(request.args.get('weight_kg'))
            frame_material = int(request.args.get('frame_material'))
    except (TypeError, ValueError):
        return jsonify({"error": "Parámetros inválidos o faltantes. Se requiere gear_count(int), weight_kg(float), frame_material(int)"}), 400

    # Crear array para predecir
    X_new = np.array([[gear_count, weight_kg, frame_material]])
    predicted_price = model_bike.predict(X_new)[0]

    return jsonify({
        "gear_count": gear_count,
        "weight_kg": weight_kg,
        "frame_material": frame_material,
        "predicted_price_usd": round(predicted_price, 2)
    })

if __name__ == "__main__":
    app.run()
