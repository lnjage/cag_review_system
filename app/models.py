from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    subjects = db.Column(db.String(200))

class Abstract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    content = db.Column(db.String(500), nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    abstract_id = db.Column(db.Integer, db.ForeignKey('abstract.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer)  # 0 to 5
    timestamp = db.Column(db.DateTime)

    user = db.relationship('User', backref='reviews')
    abstract = db.relationship('Abstract', backref='reviews')
