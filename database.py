#conexion a base de datos
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#hace conexion con la url de la bd 
#busca las variables de ese archivo y las carga como si fueran del sistema
load_dotenv()

db_url= os.getenv("db_url")

engine = create_engine(db_url)  #es el objeto que habla con post
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #plantilla para generar consultas, commit yo decido cuando guardarlos por eso False, flush controlo los cambios 
Base = declarative_base() #registro central de mis tablas 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()