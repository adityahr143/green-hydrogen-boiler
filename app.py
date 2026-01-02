import os
from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# ---------------------------
# Load trained ML model (SAFE PATH)
# ---------------------------
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "model",
    "model.pkl"
)
model = joblib.load(MODEL_PATH)

# ---------------------------
# MAIN PAGE (Landing Page)
# ---------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------------------
# PREDICTION PAGE
# ---------------------------
@app.route("/predict-page")
def predict_page():
    return render_template("predict.html")

# ---------------------------
# API: Predict Boiler Efficiency
# ---------------------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.form

        features = np.array([[
            float(data.get("feedwater_temp")),
            float(data.get("feedwater_flow")),
            float(data.get("steam_pressure")),
            float(data.get("steam_temp")),
            float(data.get("coal_flow")),
            float(data.get("oxygen_level")),
            float(data.get("flue_gas_temp")),
            float(data.get("gross_load"))
        ]])

        prediction = model.predict(features)[0]

        return jsonify({
            "efficiency": round(float(prediction), 2)
        })

    except Exception as e:
        print("PREDICTION ERROR:", e)
        return jsonify({"error": "Prediction failed"}), 500

# ---------------------------
# RUN SERVER
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
