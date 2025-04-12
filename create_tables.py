from app import create_app, db

# Create the Flask app
app = create_app()

# Drop and recreate tables in the app context
with app.app_context():
    db.drop_all()  # Drop all tables
    db.create_all()  # Create new tables
    print("✅ Tables created successfully.")
