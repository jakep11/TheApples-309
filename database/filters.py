from flask import Blueprint, request, jsonify
from sqlalchemy import and_, desc

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
   terms = data['terms']
   ids = data['ids']
   instructors = data['instructors']
   startTimes = data['timeStart']
   endTimes = data['timeEnd']

   # list of filters for the query
   filters = []

   # if no terms are selected, select the current (default) term
   if not terms:
      terms.append(Terms.query.order_by(desc(Terms.id)).first().id)

   # add term to filter
   filters.append(Sections.term_id.in_(terms))

   # add any checked filters
   if ids:
      filters.append(Sections.course_id.in_(ids))
   if instructors:
      filters.append(Sections.faculty_id.in_(instructors))
   if startTimes:
      filters.append(Sections.time_start.in_(startTimes))
   if endTimes:
      filters.append(Sections.time_end.in_(endTimes))

   sections = Sections.query.filter(and_(*filters)).all()

   return jsonify([i.serialize for i in sections])