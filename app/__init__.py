import os, pymysql, sys
from getpass import getpass
from config import Config
from flask import Blueprint, Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user

app = Flask(__name__)
app.config.from_object(Config)
app.config['DB_PASSWORD'] = getpass(prompt='DB Password: ')

def get_db_connection():
    host = app.config['DB_HOST']
    user = app.config['DB_USER']
    password = app.config['DB_PASSWORD']
    database = app.config['DATABASE']

    return pymysql.connect(host=host, user=user, password=password, database=database)

try:
    get_db_connection()

except Exception as e:
    if str(e.args[0]) == '1045':
        print('Incorrest password.')
    elif str(e.args[0]) == '2003':
        print('Connection refused on `localhost`. Please make sure the MySQL Server is running.')
    else:
        print('Unable to connect to DB: unknown error', e)
    sys.exit()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.login'

indexbp = Blueprint('index', __name__, template_folder='templates')

@indexbp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('index.home'))

    return redirect(url_for('login.login'))


@indexbp.route('/home')
def home():
    return render_template('home.html')


@indexbp.route('/about')
def about():
    return render_template('about.html')


@indexbp.route('/archive')
def archive():
    return render_template('archive.html')


@indexbp.route('/attendance')
def attendance():
    return render_template('attendance.html')


@indexbp.route('/create')
def create():
    return render_template('create.html')


@indexbp.route('/reports')
def reports():
    return redirect(url_for('reports.index'))


@indexbp.route('/support')
def support():
    return render_template('support.html')

@indexbp.route('/pending')
def pending():
    return redirect(url_for('pending.index'))



from app.views import *