import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

# ---------------------------
# Load dataset
# ---------------------------
data = pd.read_csv("dataset/industrial_dataset.csv")
print("Dataset loaded successfully")

# ---------------------------
# Select features & target
# ---------------------------
X = data[
    [
        "Feedwater temperature (℃)",
        "Feedwater flow (t/h)",
        "Main steam pressure (boiler side) (Mpa)",
        "Main steam temperature (boiler side) (℃)",
        "Coal Flow (t/h)",
        "Boiler oxygen level (%)",
        "Flue gas temperature (℃)",
        "Gross Load (MW)"
    ]
]

y = data["Boiler Eff (%)"]

# ---------------------------
# Drop missing values (IMPORTANT)
# ---------------------------
combined = pd.concat([X, y], axis=1)
combined.dropna(inplace=True)

X = combined[X.columns]
y = combined["Boiler Eff (%)"]

print("Dataset shape after cleaning:", X.shape)

# ---------------------------
# Train-test split
# ---------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------------------
# Feature scaling
# ---------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ---------------------------
# Train model
# ---------------------------
print("Training started...")
model = LinearRegression()
model.fit(X_train_scaled, y_train)
print("Training completed")

# ---------------------------
# Evaluate model
# ---------------------------
y_pred = model.predict(X_test_scaled)
r2 = r2_score(y_test, y_pred)
print("Model R² Score:", r2)

# ---------------------------
# Save model + scaler
# ---------------------------
joblib.dump((model, scaler), "model/model.pkl")
print("Model trained and saved as model.pkl")
