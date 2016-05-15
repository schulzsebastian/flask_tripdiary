from app import db, bcrypt
from geoalchemy2 import Geometry

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.user_id)

    def get_username(self):
        return unicode(self.username)

    def __repr__(self):
        return '<user %s>' % self.username

class Point(db.Model):
    __tablename__ = 'points'

    id = db.Column(db.Integer, primary_key=True)
    geom = db.Column(Geometry('Point'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self, geom, user_id):
        self.geom = geom
        self.user_id = user_id

    def get_geom(self):
        return self.geom

    def __repr__(self):
        return '<geom_id %s>' % self.id