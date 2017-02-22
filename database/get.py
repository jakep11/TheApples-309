from flask import make_response, Blueprint, render_template, flash, redirect, request, url_for, jsonify, json, Response
get_api = Blueprint('get_api', __name__)

from models import *
from web_app import db

@get_api.route('/terms', methods = ["GET"])
def get_terms():
	terms = Terms.query.all()
	return jsonify([i.serialize for i in terms])

@get_api.route('/instructors', methods = ["GET"])
def get_instructors():
	instructors = Faculty.query.all()
	return jsonify([i.serialize for i in instructors])

@get_api.route('/allCourses', methods = ["GET"])
def get_courses():
	courses = Courses.query.all()
	return jsonify([i.serialize for i in courses])

@get_api.route('/allComponents', methods = ["GET"])
def get_components():
	components = Components.query.all()
	return jsonify([i.serialize for i in components])

@get_api.route('/componentTypes', methods = ["GET"])
def get_component_types():
	componentTypes = ComponentTypes.query.all()
	return jsonify([i.serialize for i in componentTypes])

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


@get_api.route('/allSections', methods = ["GET"])
def get_sections():
	sections = Sections.query.all()
	return jsonify([i.serialize for i in sections])

@get_api.route('/preferences', methods = ["GET"])
def get_preferences():
    preferences = FacultyPreferences.query.all()
    return jsonify([i.serialize for i in preferences])

@get_api.route('/filterCourses', methods = ["POST"])
def get_filtered_courses():
	data = request.json
	number = data['number']

	courses = Courses.query.filter(Courses.number.like(number + '%')).all()
	return jsonify([i.serialize for i in courses])
