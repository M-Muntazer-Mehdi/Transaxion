# app/db_utils.py
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

import os


def create_db_engine(db_type=None, username=None, password=None, host=None, port=None, dbname=None, url=None):
    if url:
        return create_engine(url)

    if db_type == "postgres":
        url = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"
    elif db_type == "mysql":
        url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}"
    else:
        raise ValueError("Unsupported DB type")

    return create_engine(url)

def test_connection(engine):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError as e:
        print("DB ERROR:", e)
        return False

from sqlalchemy.orm import sessionmaker
from app.models import Base

def create_tables(engine):
    Base.metadata.create_all(bind=engine)

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
