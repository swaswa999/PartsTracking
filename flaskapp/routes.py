import os
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from logic.robotProgress import get_robot_progress
import random
from logic.partsDB import (
    add_part, get_all_parts, get_part_by_id, update_part,
    get_parts_by_person, get_parts_by_status
)
from logic.peopleDB import (
    get_all_people, get_person_by_id, get_person_by_name
)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/partsStudio')
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_accuracy_parts():
    accuracy_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'accuracyParts.txt')
    recommendations = {}
    if os.path.exists(accuracy_file):
        with open(accuracy_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) < 2:
                    continue
                machine_type = parts[0].strip().lower()
                machinist = parts[1].strip()
                recommendations.setdefault(machine_type, []).append(machinist)
    return recommendations

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/shoptime')
def shoptime():
    progress_data = get_robot_progress()
    return render_template('shoptime.html', progress_data=progress_data)

@main.route('/assignParts')
def assignParts():
    parts = get_all_parts()
    return render_template('assignParts.html', parts=parts)

@main.route('/editPart/<int:part_id>', methods=['GET', 'POST'])
def edit_part(part_id):
    names = [
        "Michi", "Nitzan", "Caroline", "Ruby", "Jacob", "Hannah", "Anna", 
        "Ava", "Tom", "Meni", "Satvik", "Antonio", "Victor", "Jesse", 
        "Erin", "Stella", "Brandon", "Johnny", "Nadia", "Fabi", "Hamza", 
        "Misha", "Kaavya", "Lucca", "Tony", "Keiss", "Alvin", "Justin", 
        "Ethan", "Andrew", "Sophie", "Parker", "David", "Riya", "Swayam", 
        "Siyona", "Holden", "Samuel", "Avanti", "Sangeet", "Tanmay", "Bani"
    ]

    part = get_part_by_id(part_id)
    people = get_all_people()

    if request.method == 'POST':
        assigned_machinist = random.choice(names)

        updated_part = {
            'name': request.form['name'],
            'photo': part[2],
            'description': request.form['description'],
            'priority': request.form.get('priority', type=int),
            'number_of_parts': request.form.get('number_of_parts', type=int),
            'machine_type': request.form.get('machine_type', ''),
            'difficulty': request.form.get('difficulty', type=int),
            'tolerance': request.form['tolerance'],
            'assigned_machinist': assigned_machinist,
            'drawing_sheet_creator': request.form['drawing_sheet_creator'],
            'mech_type': request.form.get('mech_type', ''),
            'progress': request.form.get('progress', 'Awaiting_Approval'),
            'qc_attempts': request.form.get('qc_attempts', type=int) or part[13]
        }
        update_part(part_id, updated_part)
        return redirect(url_for('main.assignParts'))

    return render_template('editPart.html', part=part, people=people)

@main.route('/addParts', methods=['GET', 'POST'])
def addParts():
    if request.method == 'POST':
        if 'photo' not in request.files or not request.files['photo']:
            return redirect(request.url)
        file = request.files['photo']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            part_name = request.form['name'].replace(' ', '_').upper()
            filename = secure_filename(f"{part_name}.pdf")
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

@main.route('/viewParts')
def viewParts():
    parts = get_all_parts()
    return render_template('viewParts.html', parts=parts)

@main.route('/viewPart/<int:part_id>')
def view_part(part_id):
    part = get_part_by_id(part_id)
    return render_template('viewPart.html', part=part)

@main.route('/stats')
def stats():
    people = get_all_people()
    return render_template('stats.html', people=people)

@main.route('/personStats/<int:person_id>')
def person_stats(person_id):
    person = get_person_by_id(person_id)
    parts = get_parts_by_person(person_id)
    completed_parts = [p for p in parts if p[12] == 'Completed']
    in_progress_parts = [p for p in parts if p[12] == 'In Progress']
    return render_template('personStats.html', person=person,
                           completed_parts=completed_parts,
                           in_progress_parts=in_progress_parts)

@main.route('/QC')
def QC():
    parts = get_parts_by_status('Awaiting_QC')
    return render_template('QC.html', parts=parts)

@main.route('/approve_qc/<int:part_id>', methods=['POST'])
def approve_qc(part_id):
    existing = get_part_by_id(part_id)
    updated = {
        'name': existing[1],
        'photo': existing[2],
        'description': existing[3],
        'priority': existing[4],
        'number_of_parts': existing[5],
        'machine_type': existing[6],
        'difficulty': existing[7],
        'tolerance': existing[8],
        'assigned_machinist': existing[9],
        'drawing_sheet_creator': existing[10],
        'mech_type': existing[11],
        'progress': 'Completed',
        'qc_attempts': existing[13]
    }
    update_part(part_id, updated)
    return redirect(url_for('main.QC'))

@main.route('/reject_qc/<int:part_id>', methods=['POST'])
def reject_qc(part_id):
    existing = get_part_by_id(part_id)
    updated = {
        'name': existing[1],
        'photo': existing[2],
        'description': existing[3],
        'priority': existing[4],
        'number_of_parts': existing[5],
        'machine_type': existing[6],
        'difficulty': existing[7],
        'tolerance': existing[8],
        'assigned_machinist': existing[9],
        'drawing_sheet_creator': existing[10],
        'mech_type': existing[11],
        'progress': 'Awaiting_Machining',
        'qc_attempts': existing[13] + 1
    }
    update_part(part_id, updated)
    return redirect(url_for('main.QC'))

@main.route('/personalPartsView/<int:person_id>')
def personal_parts_view(person_id):
    person = get_person_by_id(person_id)
    # Use person's name to fetch parts assigned to them
    parts = get_parts_by_person(person[1])
    completed_parts = [p for p in parts if p[12] == 'Completed']
    in_progress_parts = [p for p in parts if p[12] == 'In Progress']
    return render_template('personalPartsView.html',
                           person=person,
                           completed_parts=completed_parts,
                           in_progress_parts=in_progress_parts)

@main.route('/search_person')
def search_person():
    name = request.args.get('name')
    person = get_person_by_name(name)
    if person:
        parts = get_parts_by_person(person[0])
        completed_parts = [p for p in parts if p[12] == 'Completed']
        in_progress_parts = [p for p in parts if p[12] == 'In Progress']
        return render_template('personalPartsView.html', person=person,
                               completed_parts=completed_parts,
                               in_progress_parts=in_progress_parts)
    return redirect(url_for('main.stats'))

@main.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q', '')
    people = get_all_people()
    results = [person[1] for person in people if search.lower() in person[1].lower()]
    return jsonify(results)

@main.route('/updateStatus/<int:part_id>', methods=['POST'])
def update_status(part_id):
    existing = get_part_by_id(part_id)
    new_status = request.form.get('progress', existing[12])

    updated = {
        'name': existing[1],
        'photo': existing[2],
        'description': existing[3],
        'priority': existing[4],
        'number_of_parts': existing[5],
        'machine_type': existing[6],
        'difficulty': existing[7],
        'tolerance': existing[8],
        'assigned_machinist': existing[9],
        'drawing_sheet_creator': existing[10],
        'mech_type': existing[11],
        'progress': new_status,
        'qc_attempts': existing[13]
    }
    update_part(part_id, updated)
    return redirect(url_for('main.view_part', part_id=part_id))

