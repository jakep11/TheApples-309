import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import ../db.py
from app import db
#import app


#-- Description: Stores information and role type for each user of the system
class User(db.Model):							
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(32))
	last_name = db.Column(db.String(32))
	username = db.Column(db.String(32))
	password_hash = db.Column(db.String(64))
	role = db.Column(db.String(12))

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


#-- Description: Stores all courses taught by the University
class Courses(db.Model):						
	id = db.Column(db.Integer, primary_key=True)
	number = db.Column(db.Integer)
	major = db.Column(db.String(12))
	lecture_workload_units = db.Column(db.Integer)
	lecture_hours = db.Column(db.Integer)
	lab_workload_units = db.Column(db.Integer)
	lab_hours = db.Column(db.Integer)
	course_sections = db.relationship("Sections", backref="course")
	constraints = db.relationship("FacultyConstraint", backref="course")
	final_schedules = db.relationship("ScheduleFinal", backref="course")

#-- Description: Stores the terms taught by the University
class Terms(db.Model):							
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(15))
	term_sections = db.relationship("Sections", backref="term")
	constraints = db.relationship("FacultyConstraint", backref="term")
	comments = db.relationship("Comments", backref="term")
	final_schedules = db.relationship("ScheduleFinal", backref="term")


#-- Description: Stores all rooms with type and capacity
class Rooms(db.Model):							
	id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.String(32))
	capacity = db.Column(db.Integer)
	room_sections = db.relationship("Sections", backref="room")

#-- Description: Stores all sections that have occurred and are planned on the schedule
class Sections(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
	term_id = db.Column(db.Integer, db.ForeignKey("terms.id"))
	faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"))
	room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"))
	number = db.Column(db.Integer)
	section_type = db.Column(db.String(7))			# lecture of lab
	time_start = db.Column(db.Integer)
	time_end = db.Column(db.Integer)
	days = db.Column(db.String(3))					# 'MWF' or "TR"		

#-- Description: Stores all equipment types that will be used in various rooms
class Equipment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32))
	rooms = db.relationship("RoomEquipment", backref="equipment")


#-- Description: Stores what equipment is required in each room type
class RoomEquipment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	room_type = db.Column(db.Integer)
	equipment_id = db.Column(db.Integer, db.ForeignKey("equipment.id"))

#-- Description: Stores the course and section enrollment/waitlist information for what was actually offered by the University in previous quarters
class ScheduleFinal(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	term_id = db.Column(db.Integer, db.ForeignKey("terms.id"))
	course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
	number_sections = db.Column(db.Integer)
	total_enrollment = db.Column(db.Integer)
	

#-- Description: Stores all of the sections that are planned in a specific term
class ScheduleInitial(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	term = db.Column(db.Integer)
	section = db.Column(db.Integer)

#-- Description: Stores which tentative schedules have been 'published'
class PublishedSchedule(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	term = db.Column(db.Integer)

#-- Description: Stores faculty preferences for what days and times they would like to teach in a specific term 
class FacultyPreferences(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"))
	term = db.Column(db.Integer)		# Should this be a column, or a foreign key to Terms table
	day = db.Column(db.String(1))		# 'M', 'T', etc.
	time_start = db.Column(db.Time)
	time_end = db.Column(db.Time)
	preference = db.Column(db.String(15))

#-- Description: Stores what classes a faculty is allowed to teach
class FacultyConstraint(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"))
	term_id = db.Column(db.Integer, db.ForeignKey("terms.id"))
	course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
	constraint = db.Column(db.String(32))			# 'Not allowed' or 'Not desirable' or 'Allowed'

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
	from_faculty = db.Column(db.Integer, db.ForeignKey("faculty.id"))
	message = db.Column(db.Text)
	unread = db.Column(db.SmallInteger)
	time = db.Column(db.Time)





