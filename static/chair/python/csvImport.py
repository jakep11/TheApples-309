

# The functions in this file enable the department scheduler to import a CSV file containing resource information
# from the application.

from flask import Flask
from app import app, db
from database import models
import csv

# This function parses through a CSV file containing student plan data, and adds the information to the database
def importStudentData(inputFile):
   with open(inputFile, 'rb') as csvfile:
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

         # Using the collected enrollment data, set the totalEnrollment and waitlist fields
         if unmetDemand == 0:
            totalEnrolled = seatDemand
         else:
            totalEnrolled = enrollmentCapacity
            waitlist = unmetDemand

         # Create a new student planning data row in the ScheduleFinal database table
         studentData = models.ScheduleFinal(term=term, course=course, number_sections=numSections,
                                            total_enrollment=totalEnrolled, waitlist=waitlist)
         db.session.add(studentData)
         db.session.commit()

   return "all good"


# This function parses through a CSV file containing historic plan data, and adds the information to the database
def importHistoricData():
   with open('HistoricDemandDataF14.txt', 'rb') as csvfile:
      reader = csv.reader(csvfile, delimiter=',')
      for row in reader:
         print row