from web_app import app, db
from datetime import datetime
import timeCalculations
from sqlalchemy.orm import backref

#-- Description: Stores information and role type for each user of the system
class User(db.Model):                     
   id = db.Column(db.Integer, primary_key=True)
   first_name = db.Column(db.String(32))
   last_name = db.Column(db.String(32))
   username = db.Column(db.String(32))
   password_hash = db.Column(db.String(64))
   role = db.Column(db.String(12))

   @property
   def serialize(self):
      #"""Return object data in easily serializeable format"""
      return {
         'id'         : self.id,
         'first_name': self.first_name,
         'last_name': self.last_name,
         'username': self.username,
         'role': self.role
      }

#-- Description: Stores all faculty available to work 
class Faculty(db.Model):                  
   id = db.Column(db.Integer, primary_key=True)
   first_name = db.Column(db.String(32))
   last_name = db.Column(db.String(32))
   allowed_work_units = db.Column(db.Integer)
   faculty_sections = db.relationship("Sections", backref="faculty")
   preferences = db.relationship("FacultyPreferences", backref="faculty")
   course_preferences = db.relationship("FacultyCoursePreferences", backref="faculty")
   constraints = db.relationship("FacultyConstraint", backref="faculty")
   notifications = db.relationship("Notifications", backref="faculty")

   @property
   def serialize(self):
      #"""Return object data in easily serializeable format"""
      return {
      'id': self.id,
      'first_name': self.first_name,
      'last_name': self.last_name,
      'allowed_work_units' : self.allowed_work_units
      }

#-- Description: Stores all courses taught by the University
class Courses(db.Model):                  
   id = db.Column(db.Integer, primary_key=True)
   number = db.Column(db.Integer)
   major = db.Column(db.String(12))
   course_name = db.Column(db.String(100))
   components = db.relationship("Components", backref="course")
   course_sections = db.relationship("Sections", backref="course")
   constraints = db.relationship("FacultyConstraint", backref="course")
   final_schedules = db.relationship("ScheduleFinal", backref="course")
   student_planning_data = db.relationship("StudentPlanningData", backref="course")
   course_preferences = db.relationship("FacultyCoursePreferences", backref="course")

   @property
   def serialize(self):
      #"""Return object data in easily serializeable format"""
      return {
      'id'         : self.id,
      'number': self.number,
      'major': self.major,
      'course_name': self.course_name
      #'components': self.components
      #'course_sections': self.course_sections,
      #'constraints': self.constraints,
      #'final_schedules': self.final_schedules,
      }


#-- Description: Stores the names of the files that have been imported into the system
class Files(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(32))

#-- Description: Stores the terms taught by the University
class Terms(db.Model):                    
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(64))
   term_sections = db.relationship("Sections", backref="term")
   constraints = db.relationship("FacultyConstraint", backref="term")
   comments = db.relationship("Comments", backref="term")
   final_schedules = db.relationship("ScheduleFinal", backref="term")
   preferences = db.relationship("FacultyPreferences", backref="term")
   course_preferences = db.relationship("FacultyCoursePreferences", backref="term")
   student_planning_data = db.relationship("StudentPlanningData", backref="term")
   schedules = db.relationship("Schedule", backref="term")

   @property
   def serialize(self):

      # set quarterId and year for sorting purposes. quarterId: fall = 0, winter = 1, spring = 2
      term = self.name.split()
      quarter = term[0]
      year = int(term[2])
      quarterId = 0

      if quarter == "Winter":
         quarterId = 1
      elif quarter == "Spring":
         quarterId = 2

      #"""Return object data in easily serializeable format"""
      return {
      'id'  : self.id,
      'name': self.name,
      'quarterId': quarterId,
      'year': year
      }


#-- Description: Stores all rooms with type and capacity
class Rooms(db.Model):                    
   id = db.Column(db.Integer, primary_key=True)
   number = db.Column(db.String(32))
   type = db.Column(db.String(32))
   capacity = db.Column(db.Integer)
   room_sections = db.relationship("Sections", backref="room")
   room_equipment = db.relationship("RoomEquipment", backref="room")

#-- Description: Stores all sections that have occurred and are planned on the schedule
class Sections(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
   term_id = db.Column(db.Integer, db.ForeignKey("terms.id"))
   faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"))
   room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"))
   number = db.Column(db.Integer)
   section_type = db.Column(db.String(7))       # lecture of lab
   time_start = db.Column(db.Integer)
   time_end = db.Column(db.Integer)
   days = db.Column(db.String(3))               # 'MWF' or "TR"
   schedule_id = db.Column(db.Integer, db.ForeignKey("schedule.id"))

   # want course name, faculty name, room number,
   @property
   def serialize(self):
      #"""Return object data in easily serializeable format"""
      return {
      'id': self.id,
      'course': (Courses.query.filter_by(id=self.course_id).first()).major,
      'course_num': (Courses.query.filter_by(id=self.course_id).first()).number,
      'term_id': self.term_id,
      'faculty': (Faculty.query.filter_by(id=self.faculty_id).first()).last_name, #faculty name
      'room': (Rooms.query.filter_by(id=self.room_id).first()).number, #room number/id
      'number': self.number,
      'section_type': self.section_type,
      'time_start': timeCalculations.twelveHourTime(self.time_start),
      'time_end': timeCalculations.twelveHourTime(self.time_end),
      'hours': timeCalculations.hoursBetween(self.time_end, self.time_start),
      'days': self.days,
      'capacity': (Rooms.query.filter_by(id=self.room_id).first()).capacity
      }

#-- Description: Stores all equipment types that will be used in various rooms
class Equipment(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(32))

#-- Description: Stores what equipment is required in each room type
class RoomEquipment(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"))
   equipment_id = db.Column(db.Integer, db.ForeignKey("equipment.id"))

#-- Description: Stores the course and section enrollment/waitlist information for what was actually offered by the University in previous quarters
class ScheduleFinal(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   term_id = db.Column(db.Integer, db.ForeignKey("terms.id"))
   course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
   number_sections = db.Column(db.String(4))
   total_enrollment = db.Column(db.String(4))
   waitlist = db.Column(db.String(4))

#-- Description: Stores the student planning data information imported from CSV
class StudentPlanningData(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   term_id = db.Column(db.Integer, db.ForeignKey("terms.id"))
   course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
   number_sections = db.Column(db.Integer)
   capacity = db.Column(db.Integer)
   seat_demand = db.Column(db.Integer)
   unmet_seat_demand = db.Column(db.Integer)

#-- Description: Stores all of the sections that are scheduled in a specific term
class Schedule(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   term_id = db.Column(db.Integer, db.ForeignKey("terms.id"))
   sections = db.relationship("Sections", backref="schedule")
   published = db.Column(db.Boolean)

#-- Description: Stores faculty preferences for what days and times they would like to teach in a specific term 
class FacultyPreferences(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"))
   term_id = db.Column(db.Integer, db.ForeignKey("terms.id"))     
   day = db.Column(db.String(1))    # 'M', 'T', etc.
   time_start = db.Column(db.Time)
   time_end = db.Column(db.Time)
   preference = db.Column(db.String(15))
   
   @property
   def serialize(self):
      return {
         'faculty_id': self.faculty_id,
         'day': self.day,
         'time_start': self.time_start.isoformat()[:-3],  #[:-3] Removes the seconds from time
         'time_end': self.time_end.isoformat()[:-3],  #[:-3] Removes the seconds from time
         'choice': self.preference
      }
         
# #-- Description: Stores faculty course preferences for what classes they would like to teach
class FacultyCoursePreferences(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"))
   term_id = db.Column(db.Integer, db.ForeignKey("terms.id"))
   course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
   preference = db.Column(db.String(1)) # M - Most wanted, A - able to teach, C - cannot teach
   
   @property
   def serialize(self):
      return {
         'faculty_id': self.faculty_id,
         'course_name': self.course_name,
         'preference': self.preference
      }

#-- Description: Stores what classes a faculty is allowed to teach
class FacultyConstraint(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"))
   term_id = db.Column(db.Integer, db.ForeignKey("terms.id"))
   course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
   constraint = db.Column(db.String(32))        # 'Not allowed' or 'Not desirable' or 'Allowed'

#-- Description: Stores comments for a schedule of a given term
class Comments(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   term_id = db.Column(db.Integer, db.ForeignKey("terms.id"))
   username = db.Column(db.String(32))
   comment = db.Column(db.Text)
   time = db.Column(db.Time)

#-- Description: Stores notifications for the scheduler about changing preferences & new comments
class Notifications(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"))
   message = db.Column(db.Text)
   unread = db.Column(db.SmallInteger)
   time = db.Column(db.Time)

# -- Description: Stores the components of each of the courses
class Components(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(20))
   course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
   workload_units = db.Column(db.String(5))
   hours = db.Column(db.String(5))

   @property
   def serialize(self):
      #"""Return object data in easily serializeable format"""
      return {
      'id': self.id,
      'name': self.name,
      'course_id': self.course_id,
      'workload_units': self.workload_units,
      'hours': self.hours
      }

# -- Description: Stores the names of the imported CSV files
class ImportedFiles(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(40))

# -- Description: Stores the student cohort data
class CohortData(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
   major = db.Column(db.String(12))
   freshman = db.Column(db.Integer)
   sophmores = db.Column(db.Integer)
   juniors = db.Column(db.Integer)
   seniors = db.Column(db.Integer)

# -- Description: Stores the component types
class ComponentTypes(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(20))

   @property
   def serialize(self):
      #"""Return object data in easily serializeable format"""
      return {
      'id': self.id,
      'name': self.name,
      }