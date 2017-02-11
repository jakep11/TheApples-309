from flask import Blueprint, request, jsonify, json
import sys

# blueprint url prefix = "/filter"
filters_api = Blueprint('filters_api', __name__)

from models import *

# grab filtered courses
@filters_api.route('/courses', methods = ["GET"])
def filtered_courses():
   courses = Courses.query.all()
   return jsonify([i.serialize for i in courses])

# grab filtered sections
@filters_api.route('/sections', methods = ["POST"])
def filtered_sections():
   data = request.json
   id = data['id']


   sections = Sections.query.filter(Sections.course_id.in_(id))

   # sections = Sections.query.filter_by(course_id=67)

   print(jsonify([i.serialize for i in sections]))
   sys.stdout.flush()

   return jsonify([i.serialize for i in sections])