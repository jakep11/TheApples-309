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
	section = Sections.query.filter_by(id=id).first()
	return "Section #%d for course %s %d updated" % (section.number, section.course.major, section.course.number)

@edit_api.route('/equipment', methods = ["POST"])
def edit_equipment():
	data = request.json
	id = data['id']
	name = data['name']

	equipment = Equipment.query.filter_by(id=id).first()
	if equipment is None:
		return "ERROR EQUIPMENT NOT FOUND"
	if name is not None:
		equipment.name = name

	db.session.add(equipment)
	db.session.commit()
	equipment = Equipment.query.filter_by(id=id).first()
	return "Equipment %s updated" % (equipment.name)

@edit_api.route('/roomEquipment', methods = ["POST"])
def edit_room_equipment():
	data = request.json
	id = data['id']
	room_id = data['room_id']
	equipment_id = data['equipment_id']

	re = RoomEquipment.query.filter_by(id=id).first()
	if re is None:
		return "ERROR ROOM EQUIPMENT NOT FOUND"
	if room_id is not None:
		room = Rooms.query.filter_by(id=room_id).first()
		re.room = room
	if equipment_id is not None:
		equipment = Equipment.query.filter_by(id=equipment_id).first()
		re.equipment = equipment

	db.sesion.add(re)
	db.sesion.commit()
	re = RoomEquipment.query.filter_by(id=id).first()
	return "Room Equipment %s in room %s updated" % (room.type, equipment.name)

@edit_api.route('/scheduleFinal', methods = ["POST"])
def edit_schedule_final():
	data = request.json()
	id = data['id']
	term_id = data['term_id']
	course_id = data['course_id']
	number_sections = data['number_sections']
	total_enrollment = data['total_enrollment']
	waitlist = data['waitlist']

	sf = ScheduleFinal.query.filter_by(id=id).first()
	if sf is None:
		return "ERROR SCHEDULE FINAL NOT FOUND"
	if term_id is not None:
		term = Terms.query.filter_by(id=term_id).first()
		sf.term = term
	if course_id is not None:
		course = Courses.query.filter_by(id=course_id).first()
		sf.course = course
	if number_sections is not None:
		sf.number_sections = number_sections
	if total_enrollment is not None:
		sf.total_enrollment = total_enrollment
	if waitlist is not None:
		sf.waitlist = waitlist

	db.session.add(sf)
	db.session.commit()
	sf = ScheduleFinal.query.filter_by(id=id).first()
	return "Schedule Final with id %d updated" % (id)


@edit_api.route('/studentPlanningData', methods = ["POST"])
def edit_student_planning_data():
	data = request.json()
	id = data['id']
	term_id = data['term_id']
	course_id = data['course_id']
	number_sections = data['number_sections']
	capacity = data['capacity']
	seat_demand = data['seat_demand']
	unmet_seat_demand = data['unmet_seat_demand']

	spd = StudentPlanningData.query.filter_by(id=id).first()
	if spd is None:
		return "ERROR STUDENT PLANNING DATA NOT FOUND"
	if term_id is not None:
		term = Terms.query.filter_by(id=term_id).first()
		spd.term = term
	if course_id is not None:
		course = Courses.query.filter_by(id=course_id).first()
		spd.course = course
	if number_sections is not None:
		spd.number_sections = number_sections
	if capacity is not None:
		spd.capacity = capacity
	if seat_demand is not None:
		spd.seat_demand = seat_demand
	if unmet_seat_demand is not None:
		spd.unmet_seat_demand = unmet_seat_demand

	db.session.add(spd)
	db.session.commit()
	spd = StudentPlanningData.query.filter_by(id=id).first()
	return "Schedule Planning Data with id %d updated" % (id)

@edit_api.route('/scheduleInitial', methods = ["POST"])
def edit_schedule_initial():
	data = request.json()
	id = data['id']
	term_id = data['term_id']
	section_id = data['section_id']

	si = ScheduleInitial.query.filter_by(id=id).first()
	if si is None:
		return "ERROR SCHEDULE INITIAL NOT FOUND"
	if term_id is not None:
		term = Terms.query.filter_by(id=term_id).first()
		si.term = term
	if section_id is not None:
		section = Sections.query.filter_by(id=course_id).first()
		si.section = section

	db.session.add(si)
	db.session.commit()
	si = ScheduleInitial.query.filter_by(id=id).first()
	return "Schedule Initial with id %d updated" % (id)

@edit_api.route('/publishedSchedule', methods = ["POST"])
def edit_published_schedule():
	data = request.json()
	id = data['id']
	term_id = data['term_id']

	ps = PublishedSchedule.query.filter_by(id=id).first()
	if ps is None:
		return "ERROR PUBLISHED SCHEDULE NOT FOUND"
	if term_id is not None:
		term = Terms.query.filter_by(id=term_id).first()
		ps.term = term

	db.session.add(ps)
	db.session.commit()
	ps = PublishedSchedule.query.filter_by(id=id).first()
	return "Published Schedule with id %d updated" % (id)

@edit_api.route('/facultyPreference', methods = ["POST"])
def edit_faculty_preference():
	data = request.json()
	id = data['id']
	term_id = data['term_id']
	day = data['day']
	time_start = data['time_start']
	time_end = data['time_end']
	preference = data['preference']

	fp = FacultyPreferences.query.filter_by(id=id).first()
	if fp is None:
		return "ERROR FACULTY PREFERENCE NOT FOUND"
	if term_id is not None:
		term = Terms.query.filter_by(id=term_id).first()
		fp.term = term
	if day is not None:
		fp.day = day
	if time_start is not None:
		fp.time_start = time_start
	if time_end is not None:
		fp.time_end = time_end

	db.session.add(fp)
	db.session.commit()
	fp = FacultyPreferences.query.filter_by(id=id).first()
	return "Faculty Preference with id %d updated" % (id)

@edit_api.route('/facultyConstraint', methods = ["POST"])
def edit_faculty_constraint():
	data = request.json()
	id = data['id']
	term_id = data['term_id']
	faculty_id = data['faculty_id']
	course_id = data['course_id']
	constraint = data['constraint']

	fc = FacultyConstraint.query.filter_by(id=id).first()
	if fc is None:
		return "ERROR FACULTY CONSTRAINT NOT FOUND"
	if term_id is not None:
		term = Terms.query.filter_by(id=term_id).first()
		fc.term = term
	if faculty_id is not None:
		faculty = Faculty.query.filter_by(id=faculty_id).first()
		fc.faculty = faculty
	if course_id is not None:
		course = Courses.query.filter_by(id=course_id).first()
		fc.course = course
	if constraint is not None:
		fc.constraint = constraint

	db.session.add(fc)
	db.session.commit()
	fc = FacultyConstraint.query.filter_by(id=id).first()
	return "Faculty Constraint with id %d updated" % (id)

@edit_api.route('/comment', methods = ["POST"])
def edit_comment():
	data = request.json
	id = data['id']
	term_id = data['term_id']
	username = data['username']
	comment = data['comment']
	time = data['time']

	comment = Comments.query.filter_by(id=id).first()
	if comment is None:
		return "ERROR COMMENT NOT FOUND"
	if term_id is not None:
		term = Terms.query.filter_by(id=term_id).first()
		comment.term - term
	if username is not None:
		comment.username = username
	if time is not None:
		comment.time = time

	db.session.add(comment)
	db.session.commit()
	comment = Comments.query.filter_by(id=id).first()
	return "Comment with id %d updated" % (id)

@edit_api.route('/notification', methods = ["POST"])
def edit_notification():
	data = request.json
	id = data['id']
	faculty_id = data['faculty_id']
	message = data['message']
	unread = data['unread']
	time = data['time']

	notification = Notifications.query.filter_by(id=id).first()
	if notification is None:
		return "ERROR COMMENT NOT FOUND"
	if faculty_id is not None:
		faculty = Faculty.query.filter_by(id=faculty_id).first()
		notification.faculty = faculty
	if message is not None:
		notification.message = message
	if unread is not None:
		notification.unread = unread
	if time is not None:
		notification.time = time

	db.session.add(notification)
	db.session.commit()
	notification = Notifications.query.filter_by(id=id).first()
	return "Notification with id %d updated" % (id)




