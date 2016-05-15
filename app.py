from flask import Flask, request, url_for, redirect, render_template, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from flask.ext.bcrypt import Bcrypt
import geoalchemy2.functions as func

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_object('config.BaseConfig')
db = SQLAlchemy(app)
from models import *

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/register' , methods=['GET','POST'])
def register():
    if g.user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['username'], request.form['password'], request.form['email'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login',methods=['GET','POST'])
def login():
    if g.user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = bcrypt.generate_password_hash(request.form['password'])
    registered_user = User.query.filter_by(username=username).first()
    if registered_user is None and bcrypt.check_password_hash(password, registered_user.password):
        return redirect(url_for('login'))
    login_user(registered_user)
    return redirect(url_for('dashboard'))

@app.route('/')
def index():
    if g.user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/map')
@login_required
def map():
    points = [list(p) for p in
              db.session.query(func.ST_X(Point.geom), func.ST_Y(Point.geom)).filter_by(user_id=g.user.user_id)]
    return render_template('map.html', points=points)

@app.route('/global')
@login_required
def global_map():
    points = [list(p) for p in
              db.session.query(func.ST_X(Point.geom), func.ST_Y(Point.geom))]
    return render_template('global.html', points=points)

@app.route('/add_point/<input>')
def add_point(input):
    coordinates = list(input[7:-1].replace(" ", "").split(','))
    x = coordinates[0]
    y = coordinates[1]
    point = Point('POINT('+x+' '+y+')', g.user.user_id)
    db.session.add(point)
    db.session.commit()
    return x, y

@app.route('/delete_point/<input>')
def delete_point(input):
    coordinates = list(input[7:-1].replace(" ", "").split(','))
    x = coordinates[0]
    y = coordinates[1]
    Point.query.filter_by(geom='POINT('+x+' '+y+')', user_id=g.user.user_id).delete()
    db.session.commit()
    return x, y

if __name__ == '__main__':
    app.run()
