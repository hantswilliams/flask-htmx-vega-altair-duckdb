from flask import Blueprint, render_template

main = Blueprint('blueprint-dashboard', __name__)

@main.route('/')
def index():
    return render_template('dashboard.html')

