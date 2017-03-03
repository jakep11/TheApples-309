from flask import Blueprint, request, jsonify, json, abort
create_api = Blueprint('create_api', __name__)

from filters import roomConflict, facultyConflict
from models import *
from web_app import db

# This function adds a new user to the database. It is called when the
# system administrator clicks "create new user"
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

# This function adds a new instructor to the faculty table in the database. It is called
# when a scheduler clicks "create new instructor"
@create_api.route('/faculty', methods = ["POST"])
def new_faculty():
    data = request.json
    first_name = data['first_name']
    last_name = data['last_name']
    max_work_units = data['max_work_units']
    min_work_units = data['min_work_units']
    days = ['M', 'T', 'W', 'H', 'F']
    courses = Courses.query.all()
    print courses
    faculty = Faculty(first_name=first_name, last_name=last_name,
                        max_work_units=max_work_units, min_work_units=min_work_units)
    db.session.add(faculty)
    db.session.commit()
    for i in range(7, 22):
        for day in days:
            if i < 9:
                time_start =  "0" + str(i) + ":00"  
                time_end = "0" + str(i) + ":30" 
                fp = FacultyPreferences(faculty=faculty, day=day, time_start=time_start, time_end=time_end, preference="unavailable")
                db.session.add(fp)
                time_start = "0" + str(i) + ":30"
                time_end = "0" + str(i+1) + ":00"
                fp = FacultyPreferences(faculty=faculty, day=day, time_start=time_start, time_end=time_end, preference="unavailable")
                db.session.add(fp)
            if i == 9:
                time_start =  "0" + str(i) + ":00" 
                time_end = "09:30"
                fp = FacultyPreferences(faculty=faculty, day=day, time_start=time_start, time_end=time_end, preference="unavailable")
                db.session.add(fp)
                time_start = "09:30"
                time_end = "10:00"
                fp = FacultyPreferences(faculty=faculty, day=day, time_start=time_start, time_end=time_end, preference="unavailable")
                db.session.add(fp)
            if i > 9:
                time_start =  str(i) + ":00" 
                time_end = str(i) + ":30" 
                fp = FacultyPreferences(faculty=faculty, day=day, time_start=time_start, time_end=time_end, preference="unavailable")
                db.session.add(fp)
                time_start = str(i) + ":30"
                time_end = str(i+1) + ":00"
                fp = FacultyPreferences(faculty=faculty, day=day, time_start=time_start, time_end=time_end, preference="unavailable")
                db.session.add(fp)
    for course in courses:
        fcp = FacultyCoursePreferences(faculty=faculty, course=course, preference="C")
        db.session.add(fcp)
    db.session.commit()
    return  "Faculty added to database" 



# This function adds a new course to the course table in the database. It is called
# when a scheduler clicks "add new course"
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

# This function adds a new term to the Term table in the database. It is called
# when a scheduler clicks "add new schedule" and specifies a term
@create_api.route('/term', methods = ["POST"])
def new_term():
    data = request.json
    name = data['name']

    term = Terms(name=name)
    db.session.add(term)
    db.session.commit()
    return "Term %s added to the database" % (name)

# This function adds a new room to the Room table in the database. It is called
# when a scheduler is managing the schedule resources and clicks "add new room"
@create_api.route('/room', methods = ["POST"])
def new_room():
    data = request.json
    type = data['type']
    capacity = data['capacity']
    number = data['number']

    room = Rooms(type=type, capacity=capacity, number=number)
    db.session.add(room)
    db.session.commit()
    return " room with capacity added to database" 


# This function adds a new section to the Section table in the database. It is called
# when a scheduler is adding a new course section to a schedule for a given term
@create_api.route('/section', methods = ["POST"])
def new_section():
    data = request.json
    course_id = data.get('course_id', None)
    term_id = data.get('term_id', None)
    faculty_id = data.get('faculty_id', None)
    room_id = data.get('room_id', None)
    number = data.get('number', None)
    section_type = data.get('section_type', None)
    time_start = data.get('time_start', None)
    time_end = data.get('time_end', None)
    days = data.get('days', None)
    schedule_id = data.get('schedule.id', None) 

    test = Sections.query.filter_by(id=40).first()
    print test

    course = Courses.query.filter_by(id=course_id).first()
    if course is None:
        abort(404)
    term = Terms.query.filter_by(id=term_id).first()
    if term is None: 
        abort(404)
    faculty = Faculty.query.filter_by(id=faculty_id).first()
    if faculty is None:
        abort(404)
    room = Rooms.query.filter_by(id=room_id).first()
    if room is None:
        abort(404)
    
    # schedule = Schedule.query.filter_by(id=schedule_id).first()
    # if schedule is None:
    #     return "ERROR SCHEDULE NOT FOUND"

    
    if roomConflict(term_id, days, room_id, time_start, time_end):
        abort(406)
    if facultyConflict(term_id, days, faculty_id, time_start, time_end):
        abort(405)

    section = Sections(course=course, term=term, faculty=faculty,
                        room=room, number=number, section_type=section_type,
                        time_start=time_start, time_end=time_end, days=days)
    print "past room conflict"
    db.session.add(section)
    db.session.commit()
    return "Section added" 

# This function adds a new equipment to the Equipment table in the database. It is called
# when a scheduler clicks "add equipment"
@create_api.route('/equipment', methods = ['POST'])
def new_equipment():
    data = request.json
    name = data['name']
 
    room = Room(name=name)
    db.session.add(room)
    db.session.commit()
    return "Room %s added to database" % (room)

# This function adds a new room / equipment relationship to the roomEquipment table in the database.
# It is called when a scheduler adds an existing piece of equipment to a room.
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

# This function adds historic schedule information to the scheduleFinal table in the database. When a given term
# has passed, it's historic information is added to the db via this function.
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

# This function adds student planning data to the studentPlanningData table in the database.
# Information includes the capacity, seat demand, and unmet seat demand for a given course.
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

# This function adds a schedule to the schedule table in the database. It is called
# when a scheduler clicks "create new schedule"
@create_api.route('/schedule', methods = ['POST'])
def new_schedule():
    data = request.json
    term_name = data['name']
    #term_id = data['term_id']
    #published = data['published']

    term = Terms.query.filter_by(name=term_name).first()
    if term is None:
        newTerm = Terms(name=term_name)
        db.session.add(newTerm)
        db.session.commit()
        term = Terms.query.filter_by(name=term_name).first()

    schedule = Schedule(term=term, published=False)
    db.session.add(schedule)
    db.session.commit()
    return "Schedule added" 

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

# This function adds faculty preferences to the facultyPreferences table in the database. It is called
# when a faculty member (or a dept chair) submits preferences for a given term/
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

# This function adds a new faculty constraint to the facultyConstraint table in the database. It is called
# when a faculty member is added to the database, provided that their constraints are specified
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

# This function adds a new comment to the Comment table in the database. It is called
# when a faculty member or student sends feedback on or comments on given schedule
@create_api.route('/comment', methods = ['POST'])
def new_comment():
    data = request.json
    term_id = data['term_id']
    username = data['username']
    comment = data['comment']
    time = data['time']
    unread = data['unread']
    type = data['type']

    term = Terms.query.filter_by(id=term_id).first()
    if term is None:
        return "ERROR TERM NOT FOUND"

    comment = Comments(term=term, username=username,
                        comment=comment, time=time, unread=unread, type=type)
    db.session.add(comment)
    db.session.commit()
    return "Comment added to database"

# This function adds a new component type to the componentType table in the database. It is called
# when a scheduler clicks "add component type" under the course manager page
@create_api.route('/componentType', methods = ['POST'])
def new_component_type():
    data = request.json
    name = data['name']

    n = ComponentTypes(name=name)
    db.session.add(n)
    db.session.commit()
    return "Component Type added to database"

# This function adds a new room type to the roomType table in the database. It is called
# when a scheduler clicks "add room type" under the room manager page
@create_api.route('/roomType', methods = ['POST'])
def new_room_type():
    data = request.json
    name = data['name']

    n = RoomTypes(name=name)
    db.session.add(n)
    db.session.commit()
    return "Room Type added to database"
