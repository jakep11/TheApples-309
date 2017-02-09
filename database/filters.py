from flask import Blueprint, render_template, flash, redirect, request, url_for, jsonify, json

filters_api = Blueprint('filters_api', __name__)

from models import *
from web_app import db

# grab all courses
@filters_api.route('/allCourses', methods=["GET"])
def all_courses():
   courses = Courses.query.all()
   return jsonify([i.serialize for i in courses])


# grab filtered courses
@filters_api.route('/filteredCourses', methods=["GET"])
def filtered_courses():
   courses = Courses.query.all()
   return jsonify([i.serialize for i in courses])


# grab all sections
@filters_api.route('/allSections', methods=["GET"])
def all_sections():
   sections = Sections.query.all()
   return jsonify([i.serialize for i in sections])

# grab all sections
@filters_api.route('/filteredSections', methods=["GET"])
def filtered_sections():

   #data = request.json
   data = {
      'terms': 'Spring',
      'courses': 'CPE 309',
      'instructors': ['Kearns', 'Keen']
   };

   terms = data['terms']
   courses = data['courses']
   instructors = data['instructors']
   #startTimes = data['startTimes']
  # endTimes = data['endTimes']

   #sections = Sections.query.all()
   #return jsonify([i.serialize for i in sections])
   return jsonify(terms=terms, courses=courses, instructors=instructors)
