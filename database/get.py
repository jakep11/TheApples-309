from flask import Blueprint, render_template, flash, redirect, request, url_for, jsonify, json

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
