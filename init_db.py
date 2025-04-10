# init_db.py
from app import app, db

# Using app context to create the tables
with app.app_context():
    db.create_all()
    print("Database tables created!")
