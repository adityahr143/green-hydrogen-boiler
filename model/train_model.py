import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# -------------------------
# Path handling
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "..", "dataset", "industrial_dataset.csv")

# -------------------------
# Load Dataset
# -------------------------
data = pd.read_csv(DATASET_PATH)
print("Dataset loaded successfully")

# -------------------------
# STEP 1: Handle missing values
# -------------------------
data = data.dropna()
print("Dataset shape after dropping missing values:", data.shape)

# -------------------------
# STEP 2: Feature selection (Improved)
# -------------------------
X = data[
    [
        'Main steam pressure (boiler side) (Mpa)',
        'Main steam temperature (boiler side) (℃)',
        'Feedwater temperature (℃)',
        'Feedwater flow (t/h)',
        'Coal Flow (t/h)',
        'Boiler oxygen level (%)',
        'Flue gas temperature (℃)',
        'Gross Load (MW)'
    ]
]

y = data[['Boiler Eff (%)']]

# -------------------------
# STEP 3: Train-test split
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# -------------------------
# STEP 4: Improved model configuration
# -------------------------
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=15,
    min_samples_split=10,
    random_state=42,
    n_jobs=-1
)

print("Training started...")
model.fit(X_train, y_train.values.ravel())
print("Training completed")

# -------------------------
# Evaluation
# -------------------------
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
print("Model R² Score:", r2)

# -------------------------
# Save model
# -------------------------
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
joblib.dump(model, MODEL_PATH)

print("Model trained and saved as model.pkl")
