import os
from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load trained ML model
model = joblib.load("model/model.pkl")


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
    # logic
    return jsonify({"efficiency": round(prediction, 2)})


    try:
        features = np.array([
            data["feedwater_temp"],
            data["feedwater_flow"],
            data["main_steam_pressure"],
            data["main_steam_temp"],
            data["coal_flow"],
            data["boiler_oxygen"],
            data["flue_gas_temp"],
            data["gross_load"]
        ]).reshape(1, -1)

        prediction = model.predict(features)[0]

        return jsonify({
            "efficiency": round(prediction, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# ---------------------------
# RUN SERVER
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


