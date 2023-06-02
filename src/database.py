from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import Connector, IPTypes
from sqlalchemy import create_engine
import pymysql

# Python Connector database connection function
def getconn(user, password, database_name, connection_name):
    with Connector() as connector:
        conn = connector.connect(
            connection_name, # Cloud SQL Instance Connection Name
            "pymysql",
            user=user,
            password=password,
            db=database_name,
            ip_type= IPTypes.PUBLIC  # IPTypes.PRIVATE for private IP
        )
    return conn

# Create a SQLAlchemy engine to connect to the database
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL , creator=getconn
)

# create SQLAlchemy ORM session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()










