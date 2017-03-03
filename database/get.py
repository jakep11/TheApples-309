from flask import make_response, Blueprint, render_template, flash, redirect, request, url_for, jsonify, json, Response
from sqlalchemy import func
get_api = Blueprint('get_api', __name__)

from models import *
from web_app import db
import sys

# This function gets all the terms from the Term table in the database. It is called
# when loading the schedule in order to display the information in such a way that the scheduler
# can use the Term to filter through and view the information that has been imported into the system
@get_api.route('/terms', methods = ["GET"])
def get_terms():
	terms = Terms.query.all()
	return jsonify([i.serialize for i in terms])

# This function gets all the instructors from the Faculty table in the database. It is called
# when loading the faculty manager page from the department chairs homepage.
@get_api.route('/instructors', methods = ["GET"])
def get_instructors():
	instructors = Faculty.query.all()
	return jsonify([i.serialize for i in instructors])

# This function gets all the courses from the Course table in the database. It is called
# when loading the course manager page from the department chairs homepage.
@get_api.route('/allCourses', methods = ["GET"])
def get_courses():
	courses = Courses.query.all()
	return jsonify([i.serialize for i in courses])

# This function gets all the components from the Component table in the database. It is called
# when loading the components (labs, lectures, etc) for the courses on the course manager page.
@get_api.route('/allComponents', methods = ["GET"])
def get_components():
	components = Components.query.all()
	return jsonify([i.serialize for i in components])

# This function gets all the component types from the ComponentTypes table in the database. It is called
# when loading the course manager page from the department chairs homepage.
@get_api.route('/componentTypes', methods = ["GET"])
def get_component_types():
	componentTypes = ComponentTypes.query.all()
	return jsonify([i.serialize for i in componentTypes])

# This function gets all the rooms from the Room table in the database. It is called
# when loading the room manager page from the department chairs homepage.
@get_api.route('/roomTypes', methods = ["GET"])
def get_room_types():
	roomTypes = RoomTypes.query.all()
	return jsonify([i.serialize for i in roomTypes])

# This function gets all the file names from the ImportedFiles table in the database. It is called
# when loading the imported files from the Import CSV page from the department chairs homepage.
@get_api.route('/fileNames', methods = ["GET"])
def get_file_names():
	fileNames = ImportedFiles.query.all()
	return jsonify([i.serialize for i in fileNames])

# This function gets all the courses and components from the course and component tables in the database.
# It is called when loading the course manager page from the department chairs homepage.
@get_api.route('/allCoursesAndComponents', methods = ["GET"])
def get_courses_with_components():
	courses = Courses.query.all()

	data = []
	for course in courses:
		c1 = None
		c2 = None
		c1_hours = None
		c1_workload_units = None
		c2_hours = None
		c2_workload_units = None

		if len(course.components) > 0 :
			c1 = course.components[0].name
			c1_workload_units = course.components[0].workload_units
			c1_hours = course.components[0].hours
		if len(course.components) > 1 :
			c2 = course.components[1].name
			c2_workload_units = course.components[1].workload_units
			c2_hours = course.components[1].hours

		temp = {
			'id': course.id,
			'number': course.number,
			'major': course.major,
			'course_name': course.course_name,
			'component_one': c1,
			'c1_workload_units': c1_workload_units,
			'c1_hours': c1_hours,
			'component_two': c2,
			'c2_workload_units': c2_workload_units,
			'c2_hours': c2_hours,
		}
		data.append(temp)

	return jsonify(data)

# This function gets all the sections from the Section table in the database. It is called
# when loading a schedule for a specified term.
@get_api.route('/allSections', methods = ["GET"])
def get_sections():
	sections = Sections.query.all()
	return jsonify([i.serialize for i in sections])

# This function gets all the preferences from the Preferences table in the database. It is called
# when a department chair views the faculty preferences page.
@get_api.route('/preferences', methods = ["GET"])
def get_preferences():
   preferences = FacultyPreferences.query.all()
   return jsonify([i.serialize for i in preferences])

# This function gets all the coursePreferences from the FacultyCoursePreferences table in the database.
# It is called when viewing faculty preferences on the faculty preferences page.
@get_api.route('/coursePreferences', methods = ["GET"])
def get_course_preferences():
   course_preferences = FacultyCoursePreferences.query.all()
   return jsonify([i.serialize for i in course_preferences])

# This function gets all the courses from the Course table in the database that meet the specified filter.
#  It is called when a user wishes to filter the information in a schedule by course.
@get_api.route('/filterCourses', methods = ["POST"])
def get_filtered_courses():
	data = request.json
	course = data['filter']
	id = int(data['faculty_id'])

	courses = FacultyCoursePreferences.query.filter(Courses.course_name.contains(course)).all()
	return jsonify([i.serialize for i in courses])

# This function gets all the rooms from the Room table in the database. It is called
# when loading the room manager page from the department chairs homepage.
@get_api.route('/rooms', methods = ["GET"])
def get_rooms():
   rooms = Rooms.query.all()
   return jsonify([i.serialize for i in rooms])

# This function gets all the schedules from the Schedule table in the database. It is called
# when loading the list of schedules from the department chairs homepage.
@get_api.route('/schedules', methods = ["GET"])
def get_schedules():
   schedules = Schedule.query.all()
   return jsonify([i.serialize for i in schedules])

#This function gets a single schedule from the Schedule table in the database.
@get_api.route('/schedule', methods = ["POST"])
def get_schedule():
   data = request.json
   term_id = data.get('term_id', None)
   schedule = Schedule.query.filter_by(term_id=term_id).first()

   return jsonify(schedule.serialize)

# This function gets all the comments from the Comment table in the database. It is called
# when loading the list of notifications under the department chair's Notifications tab.
@get_api.route('/comments', methods = ["GET"])
def get_comments():
   comments = Comments.query.all()
   return jsonify([i.serialize for i in comments])

# This function gets all the instructors from the Faculty table in the database given a user ID. It is called
# when a faculty member is logged in and wishes to view their information, such as preferences or schedule.
# Given a user_id, find the faculty member associated with it
@get_api.route('/facultyFromUser', methods = ["POST"])
def get_facultyFromUser():
   data = request.json
   userID = data['userID']

   print("userID:", userID)
   sys.stdout.flush()

   user = User.query.filter_by(id=userID).first()
   faculty = Faculty.query.filter_by(first_name = user.first_name, last_name = user.last_name).first()

   print("faculty:", faculty.id)
   sys.stdout.flush()

   return jsonify(id=faculty.id, first_name=faculty.first_name, last_name=faculty.last_name)


# # This function gets the list of all faculty (with preferences) who are able and willing to teach a course
# # given a course ID. The course will be under the suitable resources column in the course manager.
# @get_api.route('/facultyFromCourse', methods = ["GET"])
# def get_facultyFromCourse():
#    data = request.json
#    courseID = data['courseId']
#
#    # Get the course that is being referenced
#    course = Courses.query.filter_by(id=courseID).first()
#
#    # Get the course that is displayed in the database
#    courseNum = course.number
#    course = Courses.query.filter_by(number=courseNum).all()
#
#
#    fcps = FacultyCoursePreferences.query.filter_by(course_id=courseID).all()
#    return jsonify([i.serialize for i in fcps])
#
#
# # This function gets the list of all rooms that are able to hold a course
# # given a course ID. The course will be under the suitable resources column in the course manager.
# @get_api.route('/roomsFromCourse', methods = ["GET"])
# def get_roomsFromCourse():
#    data = request.json
#    courseID = data['courseId']
#
#    rooms = Rooms.query.all()
#    return jsonify([i.serialize for i in rooms])
#
#
# # This function gets the student planning data for a given course
# # given a course ID. The course will be under the suitable resources column in the course manager.
# @get_api.route('/planningDataForCourse', methods = ["GET"])
# def get_planningDataForCourse():
#    data = request.json
#    courseID = data['courseId']
#
#    spd = StudentPlanningData.query.filter_by(course_id=courseID).first()
#    return jsonify(unmet_seat_demand=spd.unmet_seat_demand, seat_demand=spd.seat_demand)
#
#
# # This function gets the historic enrollment data for a given course based on a
# # given a course ID. The course will be under the suitable resources column in the course manager.
# @get_api.route('/historicDataForCourse', methods = ["GET"])
# def get_historicDataForCourse():
#    data = request.json
#    courseID = data['courseId']
#
#    historicData = ScheduleFinal.query.filter_by(course_id=courseID).all()
#    return jsonify([i.serialize for i in historicData])