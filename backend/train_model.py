# train_model.py
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import joblib
import sklearn
import os

# Dummy data for testing — you can replace this with your real dataset
data = pd.DataFrame([
    {
        "distance_from_home": 5.0,
        "distance_from_last_transaction": 1.2,
        "ratio_to_median_purchase_price": 1.5,
        "repeat_retailer": True,
        "used_chip": False,
        "used_pin_number": True,
        "online_order": False,
        "fraud": 0
    },
    {
        "distance_from_home": 100.0,
        "distance_from_last_transaction": 90.0,
        "ratio_to_median_purchase_price": 3.0,
        "repeat_retailer": False,
        "used_chip": False,
        "used_pin_number": False,
        "online_order": True,
        "fraud": 1
    }
])

X = data.drop("fraud", axis=1).astype(int)
y = data["fraud"]

model = DecisionTreeClassifier()
model.fit(X, y)

# Make sure directory exists
os.makedirs("app", exist_ok=True)

# Save the model and current sklearn version
joblib.dump(model, "app/model.pkl")
with open("app/sklearn_version.txt", "w") as f:
    f.write(sklearn.__version__)
