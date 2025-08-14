from sqlalchemy import text
from app.database import SessionLocal

db = SessionLocal()

db.execute(text("TRUNCATE TABLE recipes RESTART IDENTITY CASCADE"))
db.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
db.execute(text("TRUNCATE TABLE follows RESTART IDENTITY CASCADE"))

db.commit()
db.close()

print("Users and recipes tables cleared and IDs reset.")