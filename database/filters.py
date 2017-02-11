from flask import Blueprint, request, jsonify, json

filters_api = Blueprint('filters_api', __name__)

from models import *

# grab all courses
@filters_api.route('/allCourses', methods = ["GET"])
def all_courses():
   courses = Courses.query.all()
   return jsonify([i.serialize for i in courses])


# grab filtered courses
@filters_api.route('/filteredCourses', methods = ["GET"])
def filtered_courses():
   courses = Courses.query.all()
   return jsonify([i.serialize for i in courses])


# grab all sections
@filters_api.route('/allSections', methods = ["GET"])
def all_sections():
   sections = Sections.query.all()
   return jsonify([i.serialize for i in sections])

# grab filtered sections
@filters_api.route('/filteredSections', methods = ["POST", "GET"])
def filtered_sections():
   data = request.json
   id = data['id']

   #temporary JSON for testing purposes
   data = {
      'terms': 'Spring',
      'course_ids': [1, 5, 100, 76],
      'instructors': ['Kearns', 'Keen'],
      'startTimes': None,
      'endTimes': None
   };

   # terms = data['terms']
   # course_ids = data['course_ids']
   # instructors = data['instructors']
   # startTimes = data['startTimes']
   # endTimes = data['endTimes']

   # courses = Courses.query.filter(Courses.id.in_(data['course_ids']))


   # return jsonify([i.serialize for i in courses])
   return jsonify(id=id)