import os
from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# ---------------------------
# LOAD MODEL + SCALER (FIX)
# ---------------------------
model, scaler = joblib.load("model/model.pkl")


# ---------------------------
# MAIN PAGE
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
# API: PREDICT
# ---------------------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.form

        required_fields = [
            "feedwater_temp",
            "feedwater_flow",
            "main_steam_pressure",
            "main_steam_temp",
            "coal_flow",
            "boiler_oxygen",
            "flue_gas_temp",
            "gross_load"
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        features = np.array([
            float(data.get("feedwater_temp")),
            float(data.get("feedwater_flow")),
            float(data.get("main_steam_pressure")),
            float(data.get("main_steam_temp")),
            float(data.get("coal_flow")),
            float(data.get("boiler_oxygen")),
            float(data.get("flue_gas_temp")),
            float(data.get("gross_load"))
        ]).reshape(1, -1)

        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]

        return jsonify({"efficiency": round(prediction, 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------
# RUN SERVER
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

