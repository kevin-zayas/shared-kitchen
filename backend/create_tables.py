from app.database import Base, engine
from app import models

# Create all tables in the database
Base.metadata.create_all(bind=engine)