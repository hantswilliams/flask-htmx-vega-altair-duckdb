from flask import Blueprint, render_template

main = Blueprint('blueprint-index', __name__)

@main.route('/')
def index():
    return render_template('index.html')