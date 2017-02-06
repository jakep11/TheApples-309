from flask import Blueprint, request, jsonify, json
edit_api = Blueprint('edit_api', __name__)

from models import *
from web_app import db

@edit_api.route('/user', methods = ["POST"])
def edit_user():
    data = request.json
    id = data['id']
    username = data['username']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']

    user = User.query.filter_by(id=id).first()
    if user is None:
        return 'ERROR USER NOT FOUND'
    if username is not None:
    	user.username = username
    if password is not None:
    	user.password = password
    if first_name is not None:
    	user.first_name = first_name
    if last_name is not None:
    	user.last_name = last_name

    db.session.add(user)
    db.session.commit()
    # Re-set user variable to reflect any changes
    user = User.query.filter_by(id=id).first()
    return  "User %s updated" % (user.username)

@edit_api.route('/faculty', methods = ["POST"])
def edit_faculty():
	data = request.json
	id = data['id']
	first_name = data['first_name']
	last_name = data['last_name']
	allowed_work_units = data['allowed_work_units']

	faculty = Faculty.query.filter_by(id=id).first()
	if faculty is None:
		return 'ERROR FACULY NOT FOUND'
	if first_name is not None:
		faculty.first_name = first_name
	if last_name is not None:
		faculty.last_name = last_name
	if allowed_work_units is not None:
		faculty.allowed_work_units = allowed_work_units

	db.session.add(faculty)
	db.session.commit()
	faculty = Faculty.query.filter_by(id=id).first()
	return "Faculty %s updated" % (facutly.first_name)

@edit_api.route('/course', methods = ["POST"])
def edit_course():
	data = request.json
	id = data['id']
	number = data['number']
	major = data['major']
	lecture_workload_units = data['lecture_workload_units']
	lecture_hours = data['lecture_hours']
	lab_workload_units = data['lab_workload_units']
	lab_hours = data['lab_hours']

	course = Courses.query.filter_by(id=id).first()
	if course is None:
		return 'ERROR COURSE NOT FOUND'
	if number is not None:
		course.number = number
	if major is not None:
		course.major = major
	if lecture_workload_units is not None:
		course.lecture_workload_units = lecture_workload_units
	if lecture_hours is not None:
		course.lecture_hours = lecture_hours
	if lab_workload_units is not None:
		course.lab_workload_units = lab_workload_units
	if lab_hours is not None:
		course.lab_hours = lab_hours

	db.session.add(course)
	db.session.commit()
	course = Courses.query.filter_by(id=id).first()
	return "Course %s %d updated" % (course.major, course.number)

@edit_api.route('/term', methods = ["POST"])
def edit_term():
	data = request.json
	id = data['id']
	name = data['name']

	term = Terms.query.filter_by(id=id).first()
	if term is None:
		return 'ERROR TERM NOT FOUND'
	if name is not None:
		term.name = name

	db.session.add(term)
	db.session.commit()
	term - Terms.query.filter_by(id=id).first()
	return "Term %s updated" % (term.name)

@edit_api.route('/room', methods = ["POST"])
def edit_room():
	data = request.json
	id = data['id']
	type = data['type']
	capacity = data['capacity']

	room = Rooms.query.filter_by(id=id).first()
	if room is None:
		return 'ERROR ROOM NOT FOUND'
	if type is not None:
		room.type = type
	if capacity is not None:
		room.capacity = capacity

	db.session.add(room)
	db.session.commit()
	room = Rooms.query.filter_by(id=id).first()
	return "Room %s with capacity %d updated" % (room.type, room.capacity)

@edit_api.route('/section', methods = ["POST"])
def edit_section():
	data = request.json
	id = data['id']
	course_id = data['course_id']
	term_id = data['term_id']
	faculty_id = data['faculty_id']
	room_id = data['room_id']
	number = data['number']
	section_type = data['section_type']
	time_start = data['time_start']
	time_end = data['time_end']
	days = data['days']

	section = Sections.query.filter_by(id=id).first()
	if section is None:
		return 'ERROR SECTION NOT FOUND'
	if course_id is not None:
		course = Courses.query.filter_by(id=course_id).first()
		section.course = course
	if term_id is not None:
		term = Terms.query.filter_by(id=term_id).first()
		section.term = term
	if faculty_id is not None:
		faculty = Faculty.query.filter_by(id=faculty_id).first()
		section.faculty = faculty
	if room_id is not None:
		room = Rooms.query.filter_by(id=room_id).first()
		seciton.room = room
	if number is not None:
		section.number = number
	if section_type is not None:
		section.section_type = section_type
	if time_start is not None:
		section.time_start = time_start
	if time_end is not None:
		section.time_end = time_end
	if days is not None:
		section.days = days

	db.session.add(section)
	db.session.commit()
	section = sections.query.filter_by(id=id).first()
	return "Section #%d for course %s %d updated" % (section.number, section.course.major, section.course.number)

@edit_api.route('/equipment', methods = ["POST"])
def edit_equipment():
	data = request.json
	id = data['id']
	name = data['name']

	equipment = Equipment.query.filter_by(id=id)
	if equipment is None:
		return "ERROR EQUIPMENT NOT FOUND"
	if name is not None:
		equipment.name = name

	db.session.add(equipment)
	db.session.commit()
	equipment = Equipment.query.filter_by(id=id)
	return "Equipment %s updated" % (equipment.name)

