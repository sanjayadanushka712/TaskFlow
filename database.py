from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg://alexa@localhost/taskflow"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)