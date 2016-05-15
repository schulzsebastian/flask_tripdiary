from app import db
from models import User, Point

db.create_all()

'''
db.session.add(User("admin", "admin", "admin@admin.com"))
db.session.add(User("test", "test", "test@test.com"))
db.session.add(Point('POINT(0.0 0.0)', 1))
db.session.add(Point('POINT(10.0 10.0)', 2))
db.session.add(Point('POINT(20.0 20.0)', 1))
db.session.add(Point('POINT(30.0 30.0)', 2))
'''

db.session.commit()