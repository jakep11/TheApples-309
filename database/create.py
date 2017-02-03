from flask import Blueprint, request, jsonify, json
import bcrypt
create_api = Blueprint('create_api', __name__)

from models import *
from web_app import db

@create_api.route('/user', methods = ["POST"])
def new_user():
    data = request.json
    username = data['username']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']

    user = models.query.filter_by(username=username).first()
    if user is not None:
        return 'ERROR USERNAME ALREADY EXISTS'
    else:
        user = models.User(username=username, password=password,
                            first_name = first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()
        return  "User %s added to database" (username)

@create_api.route('/faculty', method = ["POST"])
def new_faculty():
    data = request.json
    first_name = data['first_name']
    last_name = data['last_name']
    allowed_work_units = data['allowed_word_units']

    faculty = models.Faculty(first_name=first_name, last_name=last_name,
                                allowed_word_units=allowed_word_units)
    db.session.add(faculty)
    db.session.commit()
    return  "Faculty %s %s added to database" (first_name, last_name)

@create_api.route('/course', method = ["POST"])
def new_course():
    data = request.json
    number = data['number']
    major = data['major']
    lecture_workload_units = data['lecture_workload_units']
    lecture_hours = data['lecture_hours']
    lab_workload_units = data['lab_workload_units']
    lab_hours = data['lab_hours']

    course = models.Courses(data=data, number=number, major=major,
                            lecture_workload_units=lecture_workload_units,
                            lecture_hours=lecture_hours,
                            lab_workload_units=lab_workload_units, lab_hours=lab_hours)
    db.session.add(course)
    db.session.commit()
    return  "Course %s %d added to database" % (major, number)

@create_api.route('/term', method = ["POST"])
def new_term():
    data = request.json
    name = data['name']

    term = models.Terms(name=name)
    db.session.add(term)
    db.session.commit()
    return "Term %s added to the database" % (name)

@create_api.route('/room', method = ["POST"])
def new_room():
    data = request.json
    type = data['type']
    capacity = data['capacity']

    room = models.Rooms(type=type, capacity=capacity)
    return "%s room with capacity %d added to database" % (type, capacity)

@create_api.route('/section', method = ["POST"])
def new_section():
    data = request.json
    course_id = data['course_id']
    term_id = data['term_id']
    faculty_id = data['faculty_id']
    room_id = data['room_id']
    number = data['number']
    section_type = data['section_type']
    time_start = data['time_start']
    time_end = data['time_end']
    days = data['days']

    course = models.Courses.query.filter_by(id=course_id).first()
    if course is None:
        return "ERROR COURSE NOT FOUND"
    term = models.Terms.query.filter_by(id=term_id).first()
    if term in None:
        return "ERROR TERM NOT FOUND"
    faculty = models.Faculty.query.filter_by(id=faculty_id).first()
    if faculty is None:
        return "ERROR FACULTY NOT FOUND"
    room = models.ROOMS.query.faculty_by(id=room_id).first()
    if room is None:
        return "ERROR ROOM NOT FOUND"

    section = models.Sections(course=course, term=term, faculty=faculty,
                                room=room, number=number, section_type=section_type,
                                time_start=time_start, time_end=time_end, days=days)
    db.session.add(section)
    db.session.commit()
    return "Section %d of course %s %d added to database" % (number, course.name, course.number)

@create_api.route('/equipment', method = ['POST'])
def new_equipment():
    data = request.json
    name = data['name']

    room = models.Room(name=name)
    db.session.add(room)
    db.session.commit()
    return "Room %s added to database" % (room)

@create_api.route('room_equipment', method = ['POST'])
def new_room_equipment():
    data = request.json
    room_id = data['room_id']
    equipment_id = data['equipment_id']

    room = models.Rooms.query.filter_by(id=room_id).first()
    if room is None:
        return "ERROR ROOM NOT FOUND"
    equipment = models.Equipment.query.filter_by(id=equipment_id).first()
    if equipment is None:
        return "ERROR EQUIPMENT NOT FOUND" 

    roomEquipment = models.RoomEquipment(room=room, equipment=equipment)
    db.session.add(roomEquipment)
    db.session.commit()
    return "%s added to room %s" % (equipment.name, room.type)





