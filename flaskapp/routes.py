from flask import Blueprint, render_template
from logic.robotProgress import get_robot_progress 
from logic.partsDB import add_part, get_all_parts




# Create a blueprint for main routes
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/shoptime')
def shoptime():
    progress_data = get_robot_progress()
    return render_template('shoptime.html', progress_data=progress_data)

@main.route('/viewParts')
def viewParts():
    parts = get_all_parts()
    return render_template('viewParts.html', parts=parts)

@main.route('/assignParts')
def assignParts():
    return render_template('assignParts.html')

@main.route('/addParts')
def addParts():
    return render_template('addParts.html')

@main.route('/stats')
def stats():
    return render_template('stats.html')

@main.route('/QC')
def QC():
    return render_template('QC.html')

