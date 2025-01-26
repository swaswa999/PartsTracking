from flask import Blueprint, render_template

# Create a blueprint for main routes
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/shoptime')
def shoptime():
    return render_template('shoptime.html')

@main.route('/viewParts')
def viewParts():
    return render_template('viewParts.html')

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

