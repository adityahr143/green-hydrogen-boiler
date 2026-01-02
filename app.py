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

        features = np.array([
            float(data["feedwater_temp"]),
            float(data["feedwater_flow"]),
            float(data["main_steam_pressure"]),
            float(data["main_steam_temp"]),
            float(data["coal_flow"]),
            float(data["boiler_oxygen"]),
            float(data["flue_gas_temp"]),
            float(data["gross_load"])
        ]).reshape(1, -1)

        #  VERY IMPORTANT
        features_scaled = scaler.transform(features)

        prediction = model.predict(features_scaled)[0]

        return jsonify({
            "efficiency": round(prediction, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------
# RUN SERVER
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
