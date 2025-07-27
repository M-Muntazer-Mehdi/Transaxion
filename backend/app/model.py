import joblib
import numpy as np

# Load trained model (we'll save it later as model.pkl)
model = joblib.load("app/model.pkl")

def predict_fraud(data: dict) -> int:
    """
    Accepts input data as a dictionary and returns 1 (fraud) or 0 (not fraud)
    """
    # Extract values in expected order
    features = [
        data["distance_from_home"],
        data["distance_from_last_transaction"],
        data["ratio_to_median_purchase_price"],
        int(data["repeat_retailer"]),
        int(data["used_chip"]),
        int(data["used_pin_number"]),
        int(data["online_order"]),
    ]

    prediction = model.predict([features])[0]
    return int(prediction)
