from flask import Blueprint, request, jsonify, json
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

    user = User.query.filter_by(username=username).first()
    if user is not None:
        return 'ERROR USERNAME ALREADY EXISTS'
    user = User(username=username, password=password,
                first_name = first_name, last_name=last_name)
    db.session.add(user)
    db.session.commit()
    return  "User %s added to database" (username)

@create_api.route('/faculty', methods = ["POST"])
def new_faculty():
    data = request.json
    first_name = data['first_name']
    last_name = data['last_name']
    allowed_work_units = data['allowed_word_units']

    faculty = Faculty(first_name=first_name, last_name=last_name,
                        allowed_word_units=allowed_work_units)
    db.session.add(faculty)
    db.session.commit()
    return  "Faculty %s %s added to database" (first_name, last_name)

@create_api.route('/course', methods = ["POST"])
def new_course():
    data = request.json
    number = data['number']
    major = data['major']
    course_name = data['course_name']

    component_one = data['component_one']
    c1_workload_units = data['c1_workload_units']
    c1_hours = data['c1_hours']
    component_two = data['component_two']
    c2_workload_units = data['c2_workload_units']
    c2_hours = data['c2_hours']

    course = Courses(number=number, major=major, course_name=course_name)
    db.session.add(course)
    db.session.commit()
    course = Courses.query.filter(Courses.number==number, 
        Courses.major==major, Courses.course_name==course_name).first()

    c1 = Components(course=course, name=component_one, 
        workload_units=c1_workload_units, hours=c1_hours)
    c2 = Components(course=course, name=component_two, 
        workload_units=c2_workload_units, hours=c2_hours)
                    # component_one=component_one, component_two=component_two,
                    # c1_workload_units=c1_workload_units,
                    # c1_hours=c1_hours,
                    # c2_workload_units=c2_workload_units, c2_hours=c2_hours)
    db.session.add(c1)
    db.session.add(c2)
    db.session.commit()
    return  "Course"

@create_api.route('/term', methods = ["POST"])
def new_term():
    data = request.json
    name = data['name']

    term = Terms(name=name)
    db.session.add(term)
    db.session.commit()
    return "Term %s added to the database" % (name)

@create_api.route('/room', methods = ["POST"])
def new_room():
    data = request.json
    type = data['type']
    capacity = data['capacity']
    number = data['number']

    room = Rooms(type=type, capacity=capacity, number=number)
    return "%s room with capacity %d added to database" % (type, capacity)

@create_api.route('/section', methods = ["POST"])
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
    schedule_id = data['schedule.id']

    course = Courses.query.filter_by(id=course_id).first()
    if course is None:
        return "ERROR COURSE NOT FOUND"
    term = Terms.query.filter_by(id=term_id).first()
    if term is None:
        return "ERROR TERM NOT FOUND"
    faculty = Faculty.query.filter_by(id=faculty_id).first()
    if faculty is None:
        return "ERROR FACULTY NOT FOUND"
    room = Rooms.query.filter_by(id=room_id).first()
    if room is None:
        return "ERROR ROOM NOT FOUND"
    schedule = Schedule.query.filter_by(id=schedule_id).first()
    if schedule is None:
        return "ERROR SCHEDULE NOT FOUND"

    section = Sections(course=course, term=term, faculty=faculty,
                        room=room, number=number, section_type=section_type,
                        time_start=time_start, time_end=time_end, days=days, schedule=schedule)
    db.session.add(section)
    db.session.commit()
    return "Section %d of course %s %d added to database" % (number, course.name, course.number)

@create_api.route('/equipment', methods = ['POST'])
def new_equipment():
    data = request.json
    name = data['name']

    room = Room(name=name)
    db.session.add(room)
    db.session.commit()
    return "Room %s added to database" % (room)

@create_api.route('/roomEquipment', methods = ['POST'])
def new_room_equipment():
    data = request.json
    room_id = data['room_id']
    equipment_id = data['equipment_id']

    room = Rooms.query.filter_by(id=room_id).first()
    if room is None:
        return "ERROR ROOM NOT FOUND"
    equipment = Equipment.query.filter_by(id=equipment_id).first()
    if equipment is None:
        return "ERROR EQUIPMENT NOT FOUND" 

    roomEquipment = RoomEquipment(room=room, equipment=equipment)
    db.session.add(roomEquipment)
    db.session.commit()
    return "%s added to room %s" % (equipment.name, room.type)

@create_api.route('/scheduleFinal', methods = ['POST'])
def new_schedule_final():
    data = request.json
    term_id = data['term_id']
    course_id = data['course_id']
    number_sections = data['number_sections']
    total_enrollment = data['total_enrollment']
    waitlist = data['waitlist']

    term = Terms.query.filter_by(id=term_id).first()
    if term is None:
        return "ERROR TERM NOT FOUND"
    course = Courses.query.filter_by(id=course_id).first()
    if course is None:
        return "ERROR COURSE NOT FOUND"

    sf = ScheduleFinal(term=term, course=course, number_sections=number_sections,
                        total_enrollment=total_enrollment, waitlist=waitlist)
    db.session.add(sf)
    db.session.commit()
    return "ScheduleFinal for term %s and course %s %d added to database" % (term.name, course.major, course.number)

@create_api.route('/studentPlanningData', methods = ["POST"])
def new_student_planning_data():
    data = request.json
    term_id = data['term_id']
    course_id = data['course_id']
    number_sections = data['number_sections']
    capacity = data['capacity']
    seat_demand = data['seat_demand']
    unmet_seat_demand = data['unmet_seat_demand']

    term = Terms.query.filter_by(id=term_id).first
    if term is None:
        return "ERROR TERM NOT FOUND"
    course = Courses.query.filter_by(id=course_id).first()
    if course is None:
        return "ERROR COURSE NOT FOUND"

    spd = StudentPlanningData(term=term, course=course, number_sections=number_sections,
                                capacity=capacity, seat_demand=seat_demand,
                                unmet_seat_demand=unmet_seat_demand)
    db.session.add(spd)
    db.session.commit()
    return "StudentPlanningData added to database"

@create_api.route('/schedule', methods = ['POST'])
def new_schedule():
    data = request.json
    term_id = data['term_id']
    published = data['published']

    term = Terms.query.filter_by(id=term_id).first
    if term is None:
        return "ERROR TERM NOT FOUND"

    schedule = Schedule(term_id=term, published=published)
    db.session.add(schedule)
    db.session.commit()
    return "Schedule: term %s" % (term)

# @create_api.route('publishedSchedule', methods = ['POST'])
# def new_published_schedule():
#     data = request.json
#     term_id = data['term_id']
#
#     if term_id is None:
#         return "ERROR TERM NOT FOUND"
#
#     term = Terms.query.filter_by(id=term_id).first()
#     publishedSchedule = PublishedSchedule(term=term)
#     db.session.add(publishedSchedule)
#     db.session.commit()
#     return "PublishedSchedule: term %s" % (term)

@create_api.route('/facultyPreferences', methods = ['POST'])
def new_faculty_preferences():
    data = request.json()
    faculty_id = data['faculty_id']
    term_id = data['term_id']
    day = data['day']
    time_start = data['time_start']
    time_end = data['time_end']
    preference = data['preference']

    faculty = Faculty.query.filter_by(id=faculty_id).first()
    if faculty is None:
        return "ERROR FACULTY NOT FOUND"
    term = Terms.query.filter_by(id=term.id).first()
    if term is None:
        return "ERROR TERM NOT FOUND"

    fp = FacultyPreferences(faculty=faculty, term=term, day=day,
                            time_start=time_start, time_end=time_end,
                            preference=preference)
    db.session.add(fp)
    db.session.commit()
    return "FacultyPreference added to database"

@create_api.route('/facultyConstraint', methods = ['POST'])
def new_faculty_constraint():
    data = request.json()
    faculty_id = data['faculty_id']
    term_id = data['term_id']
    course_id = data['course_id']
    constraint = data['constraint']

    faculty = Faculty.query.filter_by(id=faculty_id).first()
    if faculty is None:
        return "ERROR FACULTY NOT FOUND"
    term = Terms.query.filter_by(id=term.id).first()
    if term is None:
        return "ERROR TERM NOT FOUND"
    course = Courses.query.filter_by(id=course_id).first()
    if course is None:
        return "ERROR COURSE NOT FOUND"

    fc = facultyConstraint(faculty=faculty, term=term,
                            course=course, constraint=constraint)
    db.session.add(fc)
    db.session.commit()
    return "FacultyConstraint added to db"

@create_api.route('/comment', methods = ['POST'])
def new_comment():
    data = request.json()
    term_id = data['term_id']
    username = data['username']
    comment = data['comment']
    time = data['time']

    term = Terms.query.filter_by(id=term.id).first()
    if term is None:
        return "ERROR TERM NOT FOUND"

    comment = Comment(term=term, username=username,
                        comment=comment, time=time)
    db.session.add(comment)
    db.session.commit()
    return "Comment added to database"

@create_api.route('/notification', methods = ['POST'])
def new_notification():
    data = request.json
    faculty_id = data['faculty_id']
    message = data['message']
    unread = data['unread']
    time = data['time']

    faculty = Faculty.query.filter_by(id=faculty_id).first()
    if faculty is None:
        return "ERROR FACULTY NOT FOUND"

    n = Notification(faculty=faculty, message=message,
                        unread=unread, time=time)
    db.session.add(n)
    db.session.commit()
    return "Notification added to database"

@create_api.route('/componentType', methods = ['POST'])
def new_component_type():
    data = request.json
    name = data['name']

    n = ComponentTypes(name=name)
    db.session.add(n)
    db.session.commit()
    return "Component Type added to database"

@create_api.route('/roomType', methods = ['POST'])
def new_room_type():
    data = request.json
    name = data['name']

    n = RoomTypes(name=name)
    db.session.add(n)
    db.session.commit()
    return "Room Type added to database"
