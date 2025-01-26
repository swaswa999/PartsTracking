from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from logic.robotProgress import get_robot_progress 
from logic.partsDB import add_part, get_all_parts, get_part_by_id, update_part
from logic.peopleDB import get_all_people, get_person_by_id, get_parts_by_person

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/partsStudio')
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

@main.route('/viewPart/<int:part_id>')
def view_part(part_id):
    part = get_part_by_id(part_id)
    return render_template('viewPart.html', part=part)

@main.route('/assignParts')
def assignParts():
    parts = get_all_parts()
    return render_template('assignParts.html', parts=parts)

@main.route('/editPart/<int:part_id>', methods=['GET', 'POST'])
def edit_part(part_id):
    part = get_part_by_id(part_id)
    if request.method == 'POST':
        updated_part = {
            'description': request.form['description'],
            'priority': request.form.get('priority', type=int),
            'number_of_parts': request.form.get('number_of_parts', type=int),
            'machine_type': request.form.get('machine_type', ''),
            'difficulty': request.form.get('difficulty', type=int),
            'tolerance': request.form['tolerance'],
            'drawing_sheet_creator': request.form['drawing_sheet_creator'],
            'mech_type': request.form.get('mech_type', ''),
            'progress': request.form.get('progress', 'Awaiting_Approval'),
            'qc_attempts': 0
        }
        update_part(part_id, updated_part)
        return redirect(url_for('main.assignParts'))
    return render_template('editPart.html', part=part)

@main.route('/addParts', methods=['GET', 'POST'])
def addParts():
    if request.method == 'POST':
        if 'photo' not in request.files:
            return redirect(request.url)
        file = request.files['photo']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            part_name = request.form['name'].replace(' ', '_').upper()
            filename = secure_filename(f"{part_name}.pdf")
            
            # Ensure the upload folder exists
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
                
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            photo_path = os.path.join('static/partsStudio', filename)
            part = {
                'name': part_name,
                'photo': photo_path,
                'description': request.form['description'],
                'priority': request.form.get('priority', type=int),
                'number_of_parts': request.form.get('number_of_parts', type=int),
                'machine_type': request.form.get('machine_type', ''),
                'difficulty': request.form.get('difficulty', ''),
                'tolerance': request.form['tolerance'],
                'assigned_machinist': request.form.get('assigned_machinist', ''),
                'drawing_sheet_creator': request.form['drawing_sheet_creator'],
                'mech_type': request.form.get('mech_type', ''),
                'progress': 'Awaiting_Approval',
                'qc_attempts': 0
            }
            add_part(part)
            return redirect(url_for('main.viewParts'))
    return render_template('addParts.html')

@main.route('/stats')
def stats():
    people = get_all_people()
    return render_template('stats.html', people=people)

@main.route('/personStats/<int:person_id>')
def person_stats(person_id):
    person = get_person_by_id(person_id)
    parts = get_parts_by_person(person_id)
    completed_parts = [part for part in parts if part[6] == 'Completed']
    in_progress_parts = [part for part in parts if part[6] == 'In Progress']
    return render_template('personStats.html', person=person, completed_parts=completed_parts, in_progress_parts=in_progress_parts)

@main.route('/QC')
def QC():
    return render_template('QC.html')

@main.route('/mechView')
def mechView():
    return render_template('mechView.html')

