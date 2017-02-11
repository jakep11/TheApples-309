from web_app import app, db

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
   constraints = db.relationship("FacultyConstraint", backref="faculty")
   notifications = db.relationship("Notifications", backref="faculty")

   @property
   def serialize(self):
      #"""Return object data in easily serializeable format"""
      return {
      'id': self.id,
      'first_name': self.first_name,
      'last_name': self.last_name,
      }

#-- Description: Stores the components of each of the courses
class Components(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(20))
   #course = db.relationship("Courses", backref="component")

#-- Description: Stores all courses taught by the University
class Courses(db.Model):                  
   id = db.Column(db.Integer, primary_key=True)
   number = db.Column(db.Integer)
   major = db.Column(db.String(12))
   course_name = db.Column(db.String(100))
   component_one = db.Column(db.Integer, db.ForeignKey("components.id"))
   c1_workload_units = db.Column(db.String(5))
   c1_hours = db.Column(db.String(5))
   component_two = db.Column(db.Integer, db.ForeignKey("components.id"))
   c2_workload_units = db.Column(db.String(5))
   c2_hours = db.Column(db.String(5))
   course_sections = db.relationship("Sections", backref="course")
   constraints = db.relationship("FacultyConstraint", backref="course")
   final_schedules = db.relationship("ScheduleFinal", backref="course")
   student_planning_data = db.relationship("StudentPlanningData", backref="course")

   @property
   def serialize(self):
      #"""Return object data in easily serializeable format"""
      return {
      'id'         : self.id,
      'number': self.number,
      'major': self.major,
      'course_name': self.course_name,
      'component_one': self.component_one,
      'c1_workload_units ': self.c1_workload_units,
      'c1_hours': self.c1_hours,
      'component_two': self.component_two, 
      'c2_workload_units': self.c2_workload_units,
      'c2_hours': self.c2_hours,
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
   student_planning_data = db.relationship("StudentPlanningData", backref="term")
   published_schedules = db.relationship("PublishedSchedule", backref="term")

   @property
   def serialize(self):
      #"""Return object data in easily serializeable format"""
      return {
      'id'  : self.id,
      'name': self.name
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

   # want course name, faculty name, room number,
   @property
   def serialize(self):
      #"""Return object data in easily serializeable format"""
      return {
      'id': self.id,
      'course': (Courses.query.filter_by(id=self.course_id).first()).major,
      'course_num': (Courses.query.filter_by(id=self.course_id).first()).number,
      'term_id': (Terms.query.filter_by(id=self.term_id).first()).name, #term name
      'faculty': (Faculty.query.filter_by(id=self.faculty_id).first()).last_name, #faculty name
      'room': (Rooms.query.filter_by(id=self.room_id).first()).number, #room number/id
      'number': self.number,
      'section_type': self.section_type,
      'time_start': self.time_start,
      'time_end': self.time_end,
      'hours': (self.time_end - self.time_start) / 100,
      'days': self.days,
      'capacity': (Rooms.query.filter_by(id=self.room_id).first()).capacity
      }

#-- Description: Stores all equipment types that will be used in various rooms
class Equipment(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(32))
   rooms = db.relationship("RoomEquipment", backref="equipment")


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

#-- Description: Stores all of the sections that are planned in a specific term
class ScheduleInitial(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   term = db.Column(db.Integer)
   section = db.Column(db.Integer)

#-- Description: Stores which tentative schedules have been 'published'
class PublishedSchedule(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   term_id = db.Column(db.Integer, db.ForeignKey("terms.id"))

#-- Description: Stores faculty preferences for what days and times they would like to teach in a specific term 
class FacultyPreferences(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"))
   term_id = db.Column(db.Integer, db.ForeignKey("terms.id"))     
   day = db.Column(db.String(1))    # 'M', 'T', etc.
   time_start = db.Column(db.Time)
   time_end = db.Column(db.Time)
   preference = db.Column(db.String(15))

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





