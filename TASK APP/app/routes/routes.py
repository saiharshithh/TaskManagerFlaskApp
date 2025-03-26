from flask import Blueprint, render_template
from flask_login import login_required

global_routes = Blueprint('global', __name__)

@global_routes.route('/')
def home():
    return render_template("home.html")

@global_routes.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')