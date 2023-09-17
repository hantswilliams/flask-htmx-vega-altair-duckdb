from flask import Blueprint, render_template, jsonify
import altair as alt
import pandas as pd

main = Blueprint('blueprint-dashboard', __name__)

@main.route('/')
def index():
    return render_template('dashboard.html')

