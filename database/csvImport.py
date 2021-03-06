

# The functions in this file enable the department scheduler to import a CSV file containing resource information
# from the application.

from flask import Blueprint, request
import csv, models
import io
from web_app import db

csvImport_api = Blueprint('csvImport_api', __name__)

# This function parses through a CSV file containing student plan data, and adds the information to the database
# It is called when the chair imports a final containing the word "planning" in the title for simplicity (I know
# this is not very maintainable, but it was the easiest way to differentiate between the various types of files.
# In a later release, I would modify the following CSV importing code to be more reliable and maintainable).
@csvImport_api.route("/importStudentData", methods = ['GET', 'POST'])
def importStudentData():

   inputFile = request.files['file']
   stream = io.StringIO(inputFile.stream.read().decode("UTF8"), newline=None)
   reader = csv.reader(stream)
   rowNum = 0

   for row in reader:
      column = 0
      rowNum += 1
      print row
      for entry in row:
         column += 1

         # Term
         if column == 1 and rowNum != 1:
            term = models.Terms.query.filter_by(name=entry).first()
            if term is None: # If the term doesn't already exist, add a new term to the table
               term = models.Terms(name=entry)
               db.session.add(term)

         # Course ID
         elif column == 5 and rowNum != 1:
            courseId = entry

         # Subject Code
         elif column == 6 and rowNum != 1:
            course = models.Courses.query.filter_by(major=courseId, number=entry).first()
            if course is None: # If the course doesn't already exist, add a new course to the table
               course = models.Courses(major=courseId, number=entry)
               db.session.add(course)

         # Seat Demand
         elif column == 11 and rowNum != 1:
            seatDemand = entry

         # Sections Offered
         elif column == 12 and rowNum != 1:
            numSections = entry

         # Enrollment Capacity
         elif column == 13 and rowNum != 1:
            enrollmentCapacity = entry

         # Unmet Seat Demand
         elif column == 14 and rowNum != 1:
            unmetDemand = entry

            # Create a new student planning data row in the ScheduleFinal database table
            studentData = models.StudentPlanningData(term=term, course=course, number_sections=numSections,
                                                  capacity=enrollmentCapacity, seat_demand=seatDemand,
                                                  unmet_seat_demand=unmetDemand)

            # Add new student planning data to database
            db.session.add(studentData)
            db.session.commit()

   # upon success, add file name to database
   newfile = models.ImportedFiles.query.filter_by(name=inputFile.filename).first()
   if newfile is None:
      newfile = models.ImportedFiles(name=inputFile.filename)
      db.session.add(newfile)
      db.session.commit()

   return "successfully uploaded student planning data"


# This function parses through a CSV file containing historic plan data, and adds the information to the database
# It is called when the chair imports a final containing the word "historic" in the title
@csvImport_api.route("/importHistoricData", methods = ['GET', 'POST'])
def importHistoricData():

   inputFile = request.files['file']
   rowNumber = 0
   courseId = "CPE"
   stream = io.StringIO(inputFile.stream.read().decode("UTF8"), newline=None)
   reader = csv.reader(stream)

   for row in reader:

      rowNumber += 1

      # This is where the bulk of the information that we care about is held
      if rowNumber > 10:

         if (row[1] == "# of Sections" and row[0] != ''):
            courseNum = row[0]

            # If the course is not in the CSC/CPE Dept, figure out what dept its in. ex: DATA 301
            if len(courseNum) > 4:
               temp = courseNum.rsplit(' ', 1)
               courseId = temp[0]
               courseNum = temp[1]
               print "course num is " + courseNum
               print "course id is" + courseId

            # Set the course that the enrollment history is for
            course = models.Courses.query.filter_by(major="CPE", number=courseNum).first()
            if course is None:  # If the course doesn't exist in CPE, check CSC
               course = models.Courses.query.filter_by(major="CSC", number=courseNum).first()
               if course is None: # If the course doesn't exist in CSC or CPE, check other major
                  course = models.Courses.query.filter_by(major=courseId, number=courseNum).first()
                  if course is None: # If the course still doesn't exist, add it to the course table
                     course = models.Courses(major=courseId, number=courseNum)
                     db.session.add(course)

            # Set the terms that the enrollment history is for
            fallTerm = models.Terms.query.filter_by(name="Fall Quarter 2014").first()
            if fallTerm is None:  # If the term doesn't already exist, add a new term to the table
               fallTerm = models.Terms(name="Fall Quarter 2014")
               db.session.add(fallTerm)

            winterTerm = models.Terms.query.filter_by(name="Winter Quarter 2015").first()
            if winterTerm is None:  # If the term doesn't already exist, add a new term to the table
               winterTerm = models.Terms(name="Winter Quarter 2015")
               db.session.add(winterTerm)

            springTerm = models.Terms.query.filter_by(name="Spring Quarter 2015").first()
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

   # upon success, add file name to database
   newfile = models.ImportedFiles.query.filter_by(name=inputFile.filename).first()
   if newfile is None:
      newfile = models.ImportedFiles(name=inputFile.filename)
      db.session.add(newfile)
      db.session.commit()

   return "successfully uploaded final schedule data"

# This function parses through a CSV file containing room data, and adds the information to the database
# It is called when the chair imports a final containing the word "room" in the title
@csvImport_api.route("/importRoomData", methods = ['GET', 'POST'])
def importRoomData():

   inputFile = request.files['file']
   rowNum = 0
   stream = io.StringIO(inputFile.stream.read().decode("UTF8"), newline=None)
   reader = csv.reader(stream)

   for row in reader:
      column = 0
      for entry in row:
         column += 1

         if rowNum != 0:
            # Type
            if column == 1:
               roomType = entry

               # Checks to see if roomtype is in DB. If not, add it
               rt = models.RoomTypes.query.filter_by(name=roomType).first()

               if rt is None:
                  rt = models.RoomTypes(name=roomType)
                  # Add the new room type to the database
                  db.session.add(rt)
                  db.session.commit()

            # Number
            elif column == 2:
               roomNum = entry

            # Capacity
            elif column == 3:
               roomCapacity = entry

               # Create a new room data row in the ScheduleFinal database table
               room = models.Rooms.query.filter_by(type=roomType, number=roomNum,
                                                   capacity=roomCapacity).first()
               if room is None:
                  room = models.Rooms(type=roomType, number=roomNum, capacity=roomCapacity)

                  # Add new room data to database
                  db.session.add(room)
                  db.session.commit()

      rowNum += 1

   # upon success, add file name to database
   newfile = models.ImportedFiles.query.filter_by(name=inputFile.filename).first()
   if newfile is None:
      newfile = models.ImportedFiles(name=inputFile.filename)
      db.session.add(newfile)
      db.session.commit()

   return "successfully uploaded room data"

# This function parses through a CSV file containing course data, and adds the information to the database
# It is called when the chair imports a final containing the word "course" in the title
@csvImport_api.route("/importCourseData", methods=['GET', 'POST'])
def importCourseData():

   inputFile = request.files['file']
   stream = io.StringIO(inputFile.stream.read().decode("UTF8"), newline=None)
   reader = csv.reader(stream)

   for row in reader:

      column = 0
      comps = 0

      for entry in row:
         column += 1

         # Course dept and number
         if column == 1:
            temp = entry.rsplit(' ', 1)
            courseDept = temp[0]
            courseNum = temp[1]

         # Course name
         elif column == 2:
            courseName = entry

            # Add the new course to the database if it is not currently in there
            course = models.Courses.query.filter_by(number=courseNum, major=courseDept,
                                                 course_name=courseName).first()

            if course is None:  # If the course doesn't already exist, add a new course to the table

               # Check again if a course containing the course num and dept is in the db
               course = models.Courses.query.filter_by(number=courseNum, major=courseDept).first()

               if course is None:
                  course = models.Courses(number=courseNum, major=courseDept, course_name=courseName)
                  db.session.add(course)

               else:  # The course is in the db, but is missing a course name
                  course.course_name = courseName
                  db.session.add(course)

               db.session.commit()

         # Subject Code
         elif column > 2:
            temp = entry.rsplit(' ', 1)
            value = temp[0]
            attribute = temp[1]

            # Units
            if attribute == "unit":

               if comps == 1:
                  units = value
               else:
                  units = value

               # add component if it does not currently exist
               component = models.Components.query.filter_by(name=compName, course=course,
                                                             workload_units=units, hours=hours).first()
               if component is None:
                  component = models.Components(name=compName, course=course,
                                                workload_units=units, hours=hours)
                  db.session.add(component)
                  db.session.commit()

               # add the component type to the component type table if it does not exist
               componentType = models.ComponentTypes.query.filter_by(name=compName).first()

               if componentType is None:
                  componentType = models.ComponentTypes(name=compName)
                  db.session.add(componentType)
                  db.session.commit()

               print "made it past components"

            # Activity
            elif attribute == "activity":
               compName = "Activity"
               comps += 1
               hours = value

            # Supervisory
            elif attribute == "supv":
               compName = "Supervisory"
               comps += 1
               hours = value

            # Lecture
            elif attribute == "lect":
               compName = "Lecture"
               comps += 1
               if comps == 1:
                  hours = value
               else:
                  hours = value

            # Lab
            elif attribute == "lab":
               compName = "Lab"
               comps += 1
               if comps == 1:
                  hours = value
               else:
                  hours = value

         db.session.commit()

   # upon success, add file name to database
   newfile = models.ImportedFiles.query.filter_by(name=inputFile.filename).first()
   if newfile is None:
      newfile = models.ImportedFiles(name=inputFile.filename)
      db.session.add(newfile)
      db.session.commit()

   return "successfully uploaded course data"


# # This function parses through a CSV file containing student cohort data, and adds the information to the database
# It is called when the chair imports a final containing the word "cohort" in the title
# @csvImport_api.route("/importCohortData", methods=['GET', 'POST'])
# def importCohortData():
#
#    inputFile = request.files['file']
#    stream = io.StringIO(inputFile.stream.read().decode("UTF8"), newline=None)
#    reader = csv.reader(stream)
#
#    for row in reader:
#
#
#    # upon success, add file name to database
#    newfile = models.ImportedFiles.query.filter_by(name=inputFile.filename).first()
#    if newfile is None:
#       newfile = models.ImportedFiles(name=inputFile.filename)
#       db.session.add(newfile)
#       db.session.commit()
#
#
#    return "successfully uploaded cohort data"

# This function parses through a CSV file containing faculty data and adds it to the database
# It is called when the chair imports a final containing the word "faculty" in the title
@csvImport_api.route("/importFacultyData", methods = ['GET', 'POST'])
def importFacultyData():

   inputFile = request.files['file']
   rowNum = 0
   stream = io.StringIO(inputFile.stream.read().decode("UTF8"), newline=None)
   reader = csv.reader(stream)

   for row in reader:
      column = 0
      for entry in row:
         column += 1

         if rowNum != 0:
            # Firstname
            if column == 1:
               firstName = entry

            # Lastname
            elif column == 2:
               lastName = entry

            # Work units allowed
            elif column == 3:
               workUnits = entry

               # Create a new instructor data row in the Faculty database table
               instructor = models.Faculty.query.filter_by(first_name=firstName, last_name=lastName).first()
               if instructor is None:
                  # Add new faculty member and prefs
                  new_faculty_prefs(firstName, lastName, workUnits, 0)

      rowNum += 1

   # upon success, add file name to database
   newfile = models.ImportedFiles.query.filter_by(name=inputFile.filename).first()
   if newfile is None:
      newfile = models.ImportedFiles(name=inputFile.filename)
      db.session.add(newfile)
      db.session.commit()

   return "successfully uploaded faculty data"


# This function adds a new instructor to the faculty table in the database. It is called
# when a scheduler clicks "create new instructor"
def new_faculty_prefs(first_name, last_name, max_work_units, min_work_units):
    days = ['M', 'T', 'W', 'H', 'F']
    courses = models.Courses.query.all()
    print courses
    faculty = models.Faculty(first_name=first_name, last_name=last_name,
                        max_work_units=max_work_units, min_work_units=min_work_units, current_work_units=0)
    db.session.add(faculty)
    db.session.commit()
    for i in range(7, 22):
        for day in days:
            if i < 9:
                time_start =  "0" + str(i) + ":00"
                time_end = "0" + str(i) + ":30"
                fp = models.FacultyPreferences(faculty=faculty, day=day, time_start=time_start, time_end=time_end, preference="unavailable")
                db.session.add(fp)
                time_start = "0" + str(i) + ":30"
                time_end = "0" + str(i+1) + ":00"
                fp = models.FacultyPreferences(faculty=faculty, day=day, time_start=time_start, time_end=time_end, preference="unavailable")
                db.session.add(fp)
            if i == 9:
                time_start =  "0" + str(i) + ":00"
                time_end = "09:30"
                fp = models.FacultyPreferences(faculty=faculty, day=day, time_start=time_start, time_end=time_end, preference="unavailable")
                db.session.add(fp)
                time_start = "09:30"
                time_end = "10:00"
                fp = models.FacultyPreferences(faculty=faculty, day=day, time_start=time_start, time_end=time_end, preference="unavailable")
                db.session.add(fp)
            if i > 9:
                time_start =  str(i) + ":00"
                time_end = str(i) + ":30"
                fp = models.FacultyPreferences(faculty=faculty, day=day, time_start=time_start, time_end=time_end, preference="unavailable")
                db.session.add(fp)
                time_start = str(i) + ":30"
                time_end = str(i+1) + ":00"
                fp = models.FacultyPreferences(faculty=faculty, day=day, time_start=time_start, time_end=time_end, preference="unavailable")
                db.session.add(fp)
    for course in courses:
        fcp = models.FacultyCoursePreferences(faculty=faculty, course=course, preference="C")
        db.session.add(fcp)
    db.session.commit()
    return  "Faculty added to database"



# This function parses through a CSV file containing equipment data and adds it to the database
# It is called when the chair imports a final containing the word "equipment" in the title
@csvImport_api.route("/importEquipData", methods = ['GET', 'POST'])
def importEquipData():

   inputFile = request.files['file']
   rowNum = 0
   stream = io.StringIO(inputFile.stream.read().decode("UTF8"), newline=None)
   reader = csv.reader(stream)

   for row in reader:
      column = 0
      for entry in row:
         column += 1

         if rowNum != 0:
            # Name of equipment
            if column == 1:
               name = entry

               # Create a new equipment entry in the Equipment database table
               equip = models.Equipment.query.filter_by(name=name).first()
               if equip is None:
                  equip = models.Equipment(name=name)
                  # Add new equipment type to database
                  db.session.add(equip)
                  db.session.commit()

      rowNum += 1

   # upon success, add file name to database
   newfile = models.ImportedFiles.query.filter_by(name=inputFile.filename).first()
   if newfile is None:
      newfile = models.ImportedFiles(name=inputFile.filename)
      db.session.add(newfile)
      db.session.commit()

   return "successfully uploaded equipment data"