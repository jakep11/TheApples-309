

# The functions in this file enable the department scheduler to import a CSV file containing resource information
# from the application.

from flask import Blueprint, render_template, flash, redirect, request, url_for, jsonify, json
import csv, models
from models import *
from web_app import db

csvImport_api = Blueprint('csvImport_api', __name__)

# This function parses through a CSV file containing student plan data, and adds the information to the database
@csvImport_api.route("/importStudentData", methods = ['GET', 'POST'])
def importStudentData():
   print "in input data. Input file is "
   inputFile = request.files['file']
   print inputFile
   with open(inputFile.name, 'rb') as csvfile:
      reader = csv.reader(csvfile, delimiter=',')
      for row in reader:
         column = 0
         for entry in row:
            column += 1

            # Term
            if column == 1:
               term = models.Terms.query.filter_by(name=entry).first()
               if term is None: # If the term doesn't already exist, add a new term to the table
                  term = models.Terms(name=entry)
                  db.session.add(term)

            # Course ID
            elif column == 5:
               courseId = entry

            # Subject Code
            elif column == 6:
               course = models.Courses.query.filter_by(major=courseId, number=entry).first()
               if course is None: # If the course doesn't already exist, add a new course to the table
                  course = models.Courses(major=courseId, number=entry)
                  db.session.add(course)

            # Seat Demand
            elif column == 11:
               seatDemand = entry

            # Sections Offered
            elif column == 12:
               numSections = entry

            # Enrollment Capacity
            elif column == 13:
               enrollmentCapacity = entry

            # Unmet Seat Demand
            elif column == 14:
               unmetDemand = entry

         # Create a new student planning data row in the ScheduleFinal database table
         studentData = models.StudentPlanningData(term=term, course=course, number_sections=numSections,
                                            capacity=enrollmentCapacity, seatDemand=seatDemand, unmetSeatDemand=unmetDemand)

         # Add new student planning data to database
         db.session.add(studentData)
         db.session.commit()

   return "all good"


# This function parses through a CSV file containing historic plan data, and adds the information to the database
@csvImport_api.route("/importHistoricData/<inputFile>", methods = ['GET', 'POST'])
def importHistoricData(inputFile):
   with open(inputFile, 'rb') as csvfile:
      reader = csv.reader(csvfile, delimiter=',')
      rowNumber = 0

      for row in reader:
         rowNumber += 1
         # This is where the bulk of the information that we care about is held
         if rowNumber > 10:
            column = 1
            # If a new course information block is started
            if (len(row[column]) > 1):

               if (row[1] == "# of Sections") and (row[0] != ""):
                  courseNum = row[0]

                  # If the course is not in the CSC/CPE Dept, figure out what dept its in. ex: DATA 301
                  if len(courseNum) > 3:
                     temp = courseNum.rsplit(' ', 1)
                     courseId = temp[0]
                     courseNum = temp[1]

                  # Set the course that the enrollment history is for
                  course = models.Courses.query.filter_by(major="CPE", number=courseNum).first()
                  if course is None:  # If the course doesn't exist in CPE, check CSC
                     course = models.Courses.query.filter_by(major="CSC", number=courseNum).first()
                     if course is None: # If the course doesn't exist in CSC or CPE, check other major
                        course = models.Courses.query.filter_by(major=courseId, number=courseNum).first()
                        if course is None: # If the course still doesn't exist, add it to the course table
                           course = models.Courses(major=courseId, number=entry)
                           db.session.add(course)

                  # Set the terms that the enrollment history is for
                  fallTerm = models.Terms.query.filter_by(name="Fall Quarter 2016").first()
                  if fallTerm is None:  # If the term doesn't already exist, add a new term to the table
                     fallTerm = models.Terms(name="Fall Quarter 2014")
                     db.session.add(fallTerm)

                  winterTerm = models.Terms.query.filter_by(name="Winter Quarter 2016").first()
                  if winterTerm is None:  # If the term doesn't already exist, add a new term to the table
                     winterTerm = models.Terms(name="Winter Quarter 2015")
                     db.session.add(winterTerm)

                  springTerm = models.Terms.query.filter_by(name="Spring Quarter 2016").first()
                  if springTerm is None:  # If the term doesn't already exist, add a new term to the table
                     springTerm = models.Terms(name="Spring Quarter 2015")
                     db.session.add(springTerm)

                  # Set the term sections
                  fallSections = row[2]
                  winterSections = row[3]
                  springSections = row[4]

               # Total Enrollment data
               elif (row[1] == "Total Enrollment" and rowNumber < 400):

                  fallEnrolled = row[2]
                  winterEnrolled = row[3]
                  springEnrolled = row[4]

               # Last Waitlist data
               elif row[1] == "Last Waitlist":

                  fallWaitlist = row[2]
                  winterWaitlist = row[3]
                  springWaitlist = row[4]

                  # Add fall course history to the ScheduleFinal table
                  fallData = models.ScheduleFinal(term=fallTerm, course=course, number_sections=fallSections,
                                                           total_enrollment=fallEnrolled, waitlist=fallWaitlist)

                  # Add winter course history to the ScheduleFinal table
                  winterData = models.ScheduleFinal(term=winterTerm, course=course, number_sections=winterSections,
                                                           total_enrollment=winterEnrolled, waitlist=winterWaitlist)

                  # Add spring course history to the ScheduleFinal table
                  springData = models.ScheduleFinal(term=springTerm, course=course, number_sections=springSections,
                                                           total_enrollment=springEnrolled, waitlist=springWaitlist)

                  # Add new historic planning data to database
                  db.session.add(fallData)
                  db.session.add(winterData)
                  db.session.add(springData)
      db.session.commit()

   return "all good"

@csvImport_api.route("/importRoomData/<inputFile>", methods = ['GET', 'POST'])
def importRoomData(inputFile):
   with open(inputFile, 'rb') as csvfile:
      reader = csv.reader(csvfile, delimiter=',')
      for row in reader:
         column = 0
         for entry in row:
            column += 1

            # Type
            if column == 1:
               roomType = entry

            # Number
            elif column == 2:
               roomNum = entry

            # Capacity
            elif column == 3:
               roomCapacity = entry

         # Create a new student planning data row in the ScheduleFinal database table
         room = models.Rooms(type=roomType, number=roomNum, capacity=roomCapacity)

         # Add new student planning data to database
         db.session.add(room)
         db.session.commit()