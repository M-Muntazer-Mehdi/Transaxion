from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from app.model import predict_fraud
from app.db_utils import create_db_engine, test_connection
from sqlalchemy import text

app = FastAPI()

API_KEY = "SASCSC-SCASCASCS-SCSCS-ASCATV"

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

class TransactionInput(BaseModel):
    distance_from_home: float
    distance_from_last_transaction: float
    ratio_to_median_purchase_price: float
    repeat_retailer: bool
    used_chip: bool
    used_pin_number: bool
    online_order: bool

@app.get("/")
def read_root():
    return {"message": "Fraud Detection API is running"}

@app.post("/predict")
def predict(input: TransactionInput, _: str = Depends(verify_api_key)):
    prediction = predict_fraud(input.dict())
    return {"is_fraud": bool(prediction)}

class DBConfig(BaseModel):
    db_type: str
    username: str
    password: str
    host: str
    port: int
    dbname: str

@app.post("/test-db")
def test_db(config: DBConfig, _: str = Depends(verify_api_key)):
    try:
        engine = create_db_engine(**config.dict())
        if test_connection(engine):
            return {"status": "success", "message": "Connection successful"}
        else:
            return {"status": "fail", "message": "Connection failed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/scan-db")
def scan_db(config: DBConfig, _: str = Depends(verify_api_key)):
    try:
        engine = create_db_engine(**config.dict())
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM transactions"))
            transactions = [dict(row._mapping) for row in result]

            results = []
            for tx in transactions:
                tx_data = {
                    "distance_from_home": tx["distance_from_home"],
                    "distance_from_last_transaction": tx["distance_from_last_transaction"],
                    "ratio_to_median_purchase_price": tx["ratio_to_median_purchase_price"],
                    "repeat_retailer": tx["repeat_retailer"],
                    "used_chip": tx["used_chip"],
                    "used_pin_number": tx["used_pin_number"],
                    "online_order": tx["online_order"],
                }
                is_fraud = predict_fraud(tx_data)
                results.append({**tx, "is_fraud": bool(is_fraud)})

            return {"status": "success", "results": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}
