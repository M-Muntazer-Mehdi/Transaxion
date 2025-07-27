# app/db_utils.py
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def create_db_engine(db_type, username, password, host, port, dbname):
    if db_type == "postgres":
        url = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"
    elif db_type == "mysql":
        url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}"
    else:
        raise ValueError("Unsupported database type")
    
    engine = create_engine(url)
    return engine

def test_connection(engine):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError as e:
        print("DB ERROR:", e)
        return False
