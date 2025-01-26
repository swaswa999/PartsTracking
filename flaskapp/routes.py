from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from logic.robotProgress import get_robot_progress 
from logic.partsDB import add_part, get_all_parts

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../../data/partsPhoto')
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@main.route('/addParts', methods=['GET', 'POST'])
def addParts():
    if request.method == 'POST':
        if 'photo' not in request.files:
            return redirect(request.url)
        file = request.files['photo']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            part = {
                'name': request.form['name'],
                'photo': filename,
                'description': request.form['description'],
                'priority': request.form.get('priority', type=int),
                'number_of_parts': request.form.get('number_of_parts', type=int),
                'machine_type': request.form.get('machine_type', ''),
                'difficulty': request.form.get('difficulty', ''),
                'tolerance': request.form['tolerance'],
                'assigned_machinist': request.form.get('assigned_machinist', ''),
                'drawing_sheet_creator': request.form['drawing_sheet_creator'],
                'mech_type': request.form.get('mech_type', ''),
                'progress': request.form.get('progress', type=int)
            }
            add_part(part)
            return redirect(url_for('viewParts'))
    return render_template('addParts.html')

@main.route('/stats')
def stats():
    return render_template('stats.html')

@main.route('/QC')
def QC():
    return render_template('QC.html')

