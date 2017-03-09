from flask import Blueprint, request, jsonify, json
delete_api = Blueprint('delete_api', __name__)

from models import *
from web_app import db


# This function removes a user from the User table in the database. It is called
# when the admin selects an account to remove. 
@delete_api.route('/user', methods = ["POST"])
def delete_user():
    data = request.json
    id = data['id']

    user = User.query.filter_by(id=id).first()
    if user is None:
        return 'ERROR USER NOT FOUND'
    db.session.delete(user)
    db.session.commit()
    return  "User %s removed from database" % (user.username)

# This function removes a faculty member from the Faculty table in the database. It is called
# when the admin selects a faculty member to remove. 
@delete_api.route('/faculty', methods = ["POST"])
def delete_faculty():
    data = request.json
    id = data['id']

    faculty = Faculty.query.filter_by(id=id).first()
    if faculty is None:
        return 'ERROR FACULTY NOT FOUND'
    db.session.delete(faculty)
    db.session.commit()
    return  "Faculty %s removed from database" % (faculty.first_name)

# This function removes a course from the Course table in the database. It is called
# when the chair selects a course to remove. 
@delete_api.route('/course', methods = ["POST"])
def delete_course():
    data = request.json
    id = data['id']

    course = Courses.query.filter_by(id=id).first()
    if course is None:
        return 'ERROR COURSE NOT FOUND'
    db.session.delete(course)
    db.session.commit()
    return  "Course %s %d removed from database" % (course.major, course.number)

# This function removes a term from the Term table in the database. It is called
# when the chair selects a term to remove.
@delete_api.route('/term', methods = ["POST"])
def delete_term():
    data = request.json
    id = data['id']

    term = Terms.query.filter_by(id=id).first()
    if term is None:
        return 'ERROR TERM NOT FOUND'
    db.session.delete(term)
    db.session.commit()
    return  "Term %s removed from database" % (term.name)

# This function removes a room from the Room table in the database. It is called
# when the chair selects a room to remove.
@delete_api.route('/room', methods = ["POST"])
def delete_room():
    data = request.json
    id = data['id']

    room = Rooms.query.filter_by(id=id).first()
    if room is None:
        return 'ERROR ROOM NOT FOUND'
    db.session.delete(room)
    db.session.commit()
    return  "Room %s removed from database" % (room.type)

# This function removes a section from the Section table in the database. It is called
# when the chair selects a section to remove.
@delete_api.route('/section', methods = ["POST"])
def delete_section():
    data = request.json
    id = data['id']

    section = Sections.query.filter_by(id=id).first()
    if section is None:
        return 'ERROR SECTION NOT FOUND'
    db.session.delete(section)
    db.session.commit()
    return  "Section %d removed from database" % (section.number)

# This function removes an equipment from the Equipment table in the database. It is called
# when the chair selects an equipment to remove.
@delete_api.route('/equipment', methods = ["POST"])
def delete_equipment():
    data = request.json
    id = data['id']

    equipment = Equipment.query.filter_by(id=id).first()
    if equipment is None:
        return 'ERROR EQUIPMENT NOT FOUND'
    db.session.delete(equipment)
    db.session.commit()
    return  "Equipment %s removed from database" % (equipment.name)

# This function removes a piece of equipment from a specific room from the 
# roomEquipment table in the database. It is called when the chair selects a roomEquipment to remove.
@delete_api.route('/roomEquipment', methods = ["POST"])
def delete_room_equipment():
    data = request.json
    id = data['id']

    re = RoomEquipment.query.filter_by(id=id).first()
    if re is None:
        return 'ERROR ROOM EQUIPMENT NOT FOUND'
    db.session.delete(re)
    db.session.commit()
    return  "%s in room %s removed from database" % (re.equipment.name, re.room_type)

# This function removes a final schedule from the scheduleFinal table in the database. 
# It is called when the chair selects a final schedule to remove.
@delete_api.route('/scheduleFinal', methods = ["POST"])
def delete_schedule_final():
    data = request.json
    id = data['id']

    sf = ScheduleFinal.query.filter_by(id=id).first()
    if sf is None:
        return 'ERROR SCHEDULE FINAL NOT FOUND'
    db.session.delete(sf)
    db.session.commit()
    return  "Schedule Final: term %s course %s %d removed" % (sf.term.name, sf.course.major, sf.course.number)

# This function removes student planning data from the StudentPlanningData table in the database. 
# It is called when the chair selects some student planning data  to remove.
@delete_api.route('studentPlanningData', methods = ["POST"])
def delete_student_planning_data():
    data = request.json
    id = data['id']

    spd = StudentPlanningData.query.filter_by(id=id).first()
    if spd is None:
        return "ERROR STUDENT PLANNING DATA NOT FOUND"
    db.session.delete(spd)
    db.session.commit()
    return "Student Planning Data removed form database"

# This function removes a faculty preference from the facultyPreference table in the database. 
# It is called when the chair selects a faculty preference to remove.
@delete_api.route('/facultyPreference', methods = ["POST"])
def delete_faculty_preference():
    data = request.json
    id = data['id']

    fp = User.query.filter_by(id=id).first()
    if fp is None:
        return 'ERROR FACULTY PREFERENCE NOT FOUND'
    db.session.delete(fp)
    db.session.commit()
    return  "Faculty Preference %s removed from database" % (fp.preference)

# This function removes a faculty course preference from the facultyCoursePreference table in the database. 
# It is called when the chair selects a faculty course preference to remove.
@delete_api.route('/facultyCoursePreference', methods = ["POST"])
def delete_faculty_course_preference():
    data = request.json
    id = data['id']

    fcp = facultyCoursePreference.query.filter_by(id=id).first()
    if fcp is None:
        return 'ERROR FACULTY COURSE PREFERENCE NOT FOUND'
    db.session.delete(fcp)
    db.session.commit()
    return  "Faculty Course Preference removed from database"

# This function removes a comment from the Commnet table in the database. 
# It is called when the chair selects a comment to remove.
@delete_api.route('/comment', methods = ["POST"])
def delete_comment():
    data = request.json
    id = data['id']

    comment = Comments.query.filter_by(id=id).first()
    if comment is None:
        return 'ERROR COMMENT NOT FOUND'
    db.session.delete(comment)
    db.session.commit()
    return  "Comment %s removed from database" % (comment.comment)

# This function removes a notification from the Notification table in the database. 
# It is called when the chair selects a notification to remove.
@delete_api.route('/notification', methods = ["POST"])
def delete_notification():
    data = request.json
    id = data['id']

    notification = Notifications.query.filter_by(id=id).first()
    if notification is None:
        return 'ERROR NOTIFICATION NOT FOUND'
    db.session.delete(notification)
    db.session.commit()
    return  "Notification %s removed from database" % (notification.message)

# This function removes a component type from the componentType table in the database. 
# It is called when the chair selects a component type to remove.
@delete_api.route('/componentType', methods = ["POST"])
def delete_component_type():
    data = request.json
    id = data['id']

    componentType = ComponentTypes.query.filter_by(id=id).first()
    if componentType is None:
        return 'ERROR COMPONENT TYPE NOT FOUND'
    db.session.delete(componentType)
    db.session.commit()
    return  "Component Type %s removed from database" % (componentType.name)

# This function removes a room type from the scheduleFinal table in the database. 
# It is called when the chair selects a room type to remove.
@delete_api.route('/roomType', methods = ["POST"])
def delete_room_type():
    data = request.json
    id = data['id']

    roomType = RoomTypes.query.filter_by(id=id).first()
    if roomType is None:
        return 'ERROR ROOM TYPE NOT FOUND'
    db.session.delete(roomType)
    db.session.commit()
    return  "Room Type %s removed from database" % (roomType.name)