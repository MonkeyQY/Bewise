from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from app.Task2 import config

database_url = URL.create(**config.DATABASE_Task2)
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)

metadata = MetaData(bind=engine)
