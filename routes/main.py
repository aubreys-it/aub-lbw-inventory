
from flask import Blueprint, render_template
from flask_login import login_required
from utils.decorators import admin_required

main = Blueprint('main', __name__)

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main.route('/admin')
@login_required
@admin_required
def admin_panel():
    return render_template('admin.html')
