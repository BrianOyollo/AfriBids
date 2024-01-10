from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os 

load_dotenv()
POSTGRES_USERNAME=os.getenv('POSTGRES_USERNAME')
POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')
DATABASE_NAME=os.getenv('DATABASE_NAME')
POSTGRES_PORT=os.getenv('POSTGRES_PORT')
POSTGRES_HOST=os.getenv('POSTGRES_HOST')


SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass