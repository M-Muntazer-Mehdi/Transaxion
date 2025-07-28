from sqlalchemy import Column, Integer, Float, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PredictionResult(Base):
    __tablename__ = "fraud_predictions"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String)
    ml_prediction = Column(String)
    ml_confidence = Column(Float)
    final_risk_score = Column(Float)
    risk_level = Column(String)
    rule_high_amount = Column(Boolean)
    rule_night_time = Column(Boolean)
    rule_suspicious_country = Column(Boolean)
    total_flags = Column(Integer)
    triggered_flags = Column(String)
