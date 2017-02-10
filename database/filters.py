from flask import Blueprint, render_template, flash, redirect, request, url_for, jsonify, json
from sqlalchemy import and_

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

   #temporary JSON for testing purposes
   data = {
      'terms': 'Spring',
      'courses': ['CPE 309', 'ME 308', 'BUS 357'],
      'instructors': ['Kearns', 'Keen'],
      'startTimes': None,
      'endTimes': None
   };

   # terms = data['terms']
   # courses = data['courses']
   # instructors = data['instructors']
   # startTimes = data['startTimes']
   # endTimes = data['endTimes']

   courseMajor = []
   courseNum = []

   for c in data['courses']:
      course = c.split()
      courseMajor.append(course[0])
      courseNum.append(course[1])

   courses = Courses.query.filter(and_(Courses.major.in_(courseMajor), Courses.number.in_(courseNum))).all()

   #courses = Courses.query.filter_by(course)

   #sections = Sections.query.filter_by(course_id=1)
   #return jsonify([i.serialize for i in sections])

   #return jsonify(terms=terms, courses=courses, instructors=instructors, startTimes=startTimes, endTimes=endTimes)
   #return jsonify(courseMajor=courseMajor, courseNum=courseNum)

   return jsonify([i.serialize for i in courses])
