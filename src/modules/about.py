from flask import Blueprint, render_template

main = Blueprint('blueprint-about', __name__)

@main.route('/')
def index():
    return render_template('about.html')

