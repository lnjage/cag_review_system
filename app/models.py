from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    subjects = db.Column(db.String(200))

     # Password hashing methods
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)  

class Abstract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    content = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<Abstract {self.title}>'

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    abstract_id = db.Column(db.Integer, db.ForeignKey('abstract.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer)  # 0 to 5
    timestamp = db.Column(db.DateTime)

    user = db.relationship('User', backref='reviews')
    abstract = db.relationship('Abstract', backref='reviews')

    def __repr__(self):
        return f'<Review {self.score} for Abstract {self.abstract_id} by User {self.reviewer_id}>'
