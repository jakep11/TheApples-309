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
   # retrieve JSON data
   data = request.json
   terms = data.get('terms', None)
   ids = data.get('ids', None)
   instructors = data.get('instructors', None)
   startTimes = data.get('timeStart', None)
   endTimes = data.get('timeEnd', None)

   # list of filters for the query
   filters = []

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

def roomConflict(term_id, days, room_id, time_start, time_end):
   #need to check if there is another room on the same days, 
   #same term, and same time as this one
   filters = []  

   #Checks same room
   filters.append(Sections.room_id == room_id)

   #Grabs section from the correct term
   filters.append(Sections.term_id == term_id)

   #Checks to make sure on the same day
   filters.append(Sections.days == days)

   #Checks time
   filters.append(time_start < Sections.time_end)
   filters.append(time_end > Sections.time_start)

   sections = Sections.query.filter(and_(*filters)).all()
   
   if len(sections) >= 1:
      return True

   return False

def facultyConflict(term_id, days, faculty_id, time_start, time_end):
   #need to figure out if this faculty has another class on same day and time
   filters = []  

   #Checks same room
   filters.append(Sections.faculty_id == faculty_id)

   #Grabs section from the correct term
   filters.append(Sections.term_id == term_id)

   #Checks to make sure on the same day
   filters.append(Sections.days == days)

   #Checks time
   filters.append(time_start < Sections.time_end)
   filters.append(time_end > Sections.time_start)

   sections = Sections.query.filter(and_(*filters)).all()

   if len(sections) >= 1:
      return True

   return False 

#Function that checks if adding a section to a faculty's schedule would exceed their
#maximum allowed workload_units
def facultyWorkloadConflict(term_id, faculty_id, course_id):
   filters = []  

   #get faculty max workload
   max_workload = Faculty.query.filter_by(id=faculty_id).first().max_work_units

   #determine amount of units for section being added
   this_units = 0
   this_course = Courses.query.filter_by(id=course_id).first()
   for comp in this_course.components:
      this_units = this_units + int(comp.workload_units)

   
   #Checks same room
   filters.append(Sections.faculty_id == faculty_id)

   #Grabs section from the correct term
   filters.append(Sections.term_id == term_id)
 
 
   sections = Sections.query.filter(and_(*filters)).all()
  
   temp_units = 0

   for i in sections: 
      #print i
      for j in i.course.components:
         temp_units = temp_units + int(j.workload_units)

   total_units = temp_units + this_units
   print total_units
   if total_units > max_workload:
      return True
 
   return False