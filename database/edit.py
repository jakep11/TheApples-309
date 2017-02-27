from flask import Blueprint, request, jsonify, json
import bcrypt
from sqlalchemy import and_
edit_api = Blueprint('edit_api', __name__)

from models import *
from web_app import db

@edit_api.route('/user', methods = ["POST"])
def edit_user(): 
    data = request.json
    id = data.get('id', None)
    username = data.get('username', None) 
    password = data.get('password', None)
    print password
    first_name = data.get('first_name', None)
    last_name = data.get('last_name', None)
    role = data.get('role', None) 

    user = User.query.filter_by(id=id).first()
    if user is None:
        return 'ERROR USER NOT FOUND'
    if username is not None:
      user.username = username
    if password is not None:
      user.password_hash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
      print "changed password"
    if first_name is not None:
      user.first_name = first_name
    if last_name is not None:
      user.last_name = last_name
    if role is not None:
      user.role = role
    db.session.add(user)
    db.session.commit()
    # Re-set user variable to reflect any changes
    user = User.query.filter_by(id=id).first()
    return  "User %s updated" % (user.username)

@edit_api.route('/faculty', methods = ["POST"])
def edit_faculty():
   data = request.json
   id = data.get('id', None)
   first_name = data.get('first_name', None)
   last_name = data.get('last_name', None)
   min_work_units = data.get('min_work_units', None)
   max_work_units = data.get('max_work_units', None)

   faculty = Faculty.query.filter_by(id=id).first()
   if faculty is None:
      return 'ERROR FACULY NOT FOUND'
   if first_name is not None:
      faculty.first_name = first_name
   if last_name is not None:
      faculty.last_name = last_name
   if max_work_units is not None:
      faculty.max_work_units = max_work_units
   if min_work_units is not None:
      faculty.min_work_units = min_work_units

   db.session.add(faculty)
   db.session.commit()
   return "Faculty updated" 

@edit_api.route('/course', methods = ["POST"])
def edit_course():
   data = request.json
   id = data.get('id', None)
   number = data.get('number', None)
   major = data.get('major', None)
   course_name = data.get('course_name', None)
   component_one = data.get('component_one', None)
   c1_workload_units = data.get('c1_workload_units', None)
   c1_hours = data.get('c1_hours', None)
   component_two = data.get('component_two', None)
   c2_workload_units = data.get('c2_workload_units', None)
   c2_hours = data.get('c2_hours', None)

   course = Courses.query.filter_by(id=id).first()
   if course is None:
      return 'ERROR COURSE NOT FOUND'
   if number is not None:
      course.number = number
   if major is not None:
      course.major = major
   if course_name is not None:
      course.course_name = course_name

   db.session.add(course)
   db.session.commit()

   #Edit the components now
   components = course.components
   for comp in components:
      db.session.delete(comp)
   db.session.commit()

   if component_one is not None:
      c1 = Components(course=course, name=component_one, 
      workload_units=c1_workload_units, hours=c1_hours)
      db.session.add(c1)
   if component_two is not None:
      c2 = Components(course=course, name=component_two, 
      workload_units=c2_workload_units, hours=c2_hours)
      db.session.add(c2)

   db.session.commit()

  
   course = Courses.query.filter_by(id=id).first()
   return "Course edited"

@edit_api.route('/term', methods = ["POST"])
def edit_term():
   data = request.json
   id = data.get('id', None)
   name = data.get('name', None)

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
   id = data.get('id', None)
   type = data.get('type', None)
   capacity = data.get('capacity', None)
   number = data.get('room', None)

   room = Rooms.query.filter_by(id=id).first()
   if room is None:
      return 'ERROR ROOM NOT FOUND'
   if type is not None:
      room.type = type
   if capacity is not None:
      room.capacity = capacity
   if number is not None:
      room.number = number

   db.session.add(room)
   db.session.commit()
   room = Rooms.query.filter_by(id=id).first()
   return "Room %s with capacity %d updated" % (room.type, room.capacity)

@edit_api.route('/section', methods = ["POST"])
def edit_section():
   data = request.json
   id = data.get('id', None)
   course_id = data.get('course_id', None)
   term_id = data.get('term_id', None)
   faculty_id = data.get('faculty_id', None)
   room_id = data.get('room_id', None)
   number = data.get('number', None)
   section_type = data.get('section_type', None)
   time_start = data.get('time_start', None)
   time_end = data.get('time_end', None)
   days = data.get('days', None)
   schedule_id = data.get('schedule_id', None)

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
      section.room = room
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
   if schedule_id is not None:
      schedule = Schedule.query.filter_by(id=schedule_id).first()
      section.schedule = schedule


   db.session.add(section)
   db.session.commit()
   section = Sections.query.filter_by(id=id).first()
   return "Section #%d for course %s %d updated" % (section.number, section.course.major, section.course.number)

@edit_api.route('/equipment', methods = ["POST"])
def edit_equipment():
   data = request.json
   id = data.get('id', None)
   name = data.get('name', None)

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
   id = data.get('id', None)
   room_id = data.get('room_id', None)
   equipment_id = data.get('equipment_id', None)

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
   data = request.json
   id = data.get('id', None)
   term_id = data.get('term_id', None)
   course_id = data.get('course_id', None)
   number_sections = data.get('number_sections', None)
   total_enrollment = data.get('total_enrollment', None)
   waitlist = data.get('waitlist', None)

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
   data = request.json
   id = data.get('id', None)
   term_id = data.get('term_id', None)
   course_id = data.get('course_id', None)
   number_sections = data.get('number_sections', None)
   capacity = data.get('capacity', None)
   seat_demand = data.get('seat_demand', None)
   unmet_seat_demand = data.get('unmet_seat_demand', None)

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

@edit_api.route('/schedule', methods = ["POST"])
def edit_schedule():
   data = request.json
   id = data.get('id', None)
   term_id = data.get('term_id', None)
   published = data.get('published', None)

   s = Schedule.query.filter_by(id=id).first()
   if s is None:
      return "ERROR SCHEDULE NOT FOUND"
   if term_id is not None:
      term = Terms.query.filter_by(id=term_id).first()
      s.term = term
   if published is not None:
      s.published = published

   db.session.add(s)
   db.session.commit()
   return "Schedule with id %d updated" % (id)

# @edit_api.route('/publishedSchedule', methods = ["POST"])
# def edit_published_schedule():
#    data = request.json()
#    id = data.get('id', None)
#    term_id = data.get('term_id', None)
#
#    ps = PublishedSchedule.query.filter_by(id=id).first()
#    if ps is None:
#       return "ERROR PUBLISHED SCHEDULE NOT FOUND"
#    if term_id is not None:
#       term = Terms.query.filter_by(id=term_id).first()
#       ps.term = term
#
#    db.session.add(ps)
#    db.session.commit()
#    ps = PublishedSchedule.query.filter_by(id=id).first()
#    return "Published Schedule with id %d updated" % (id)

@edit_api.route('/facultyPreference', methods = ["POST"])
def edit_faculty_preference():
   data = request.json
   id = data.get('p_id', None)
   time_pref = data.get('time_pref', None)

   pref = time_pref.split('-')[0]

   fp = FacultyPreferences.query.filter_by(id=id).first()
   if fp is None:
      return "ERROR FACULTY PREFERENCE NOT FOUND"
   fp.preference = pref 

   db.session.add(fp)
   db.session.commit()
   fp = FacultyPreferences.query.filter_by(id=id).first()
   return "Faculty Preference with id %d updated" % (id)

@edit_api.route('/facultyConstraint', methods = ["POST"])
def edit_faculty_constraint():
   data = request.json
   id = data.get('id', None)
   term_id = data.get('term_id', None)
   faculty_id = data.get('faculty_id', None)
   course_id = data.get('course_id', None)
   constraint = data.get('constraint', None)

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

@edit_api.route('/facultyCoursePreference', methods = ["POST"])
def edit_faculty_course_preference():
   data = request.json
   cp_id = data.get('cp_id', None)
   pref = data.get('pref', None)

   fcp = FacultyCoursePreferences.query.filter_by(id=cp_id).first()
   if fcp is None:
      return "ERROR FCP NOT FOUND"
   fcp.preference = pref


   db.session.add(fcp)
   db.session.commit()
   fcp = FacultyCoursePreferences.query.filter_by(id=cp_id).first()
   return "Faculty Course Preference with id %d updated" % (cp_id)

@edit_api.route('/comment', methods = ["POST"])
def edit_comment():
   data = request.json
   id = data.get('id', None)
   term_id = data.get('term_id', None)
   username = data.get('username', None)
   comment = data.get('comment', None)
   time = data.get('time', None)

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
   id = data.get('id', None)
   faculty_id = data.get('faculty_id', None)
   message = data.get('message', None)
   unread = data.get('unread', None)
   time = data.get('time', None)

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

@edit_api.route('/saveChanges', methods = ["POST"])
def save_changes():
   data = request.json
   id = data.get('id', None)
   min_units = data.get('min_units', None)
   max_units = data.get('max_units', None)

   faculty = Faculty.query.filter_by(id=id).first()
   if faculty is None:
      return "ERROR FACULTY NOT FOUND"
   if min_units is not None:
      faculty.min_work_units = min_units
   if max_units is not None:
      faculty.max_work_units = max_units

   db.session.add(faculty)
   db.session.commit()
   faculty = Faculty.query.filter_by(id=id).first()
   return "Faculty with id %d updated" % (int(id))




