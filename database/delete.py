from flask import Blueprint, request, jsonify, json
delete_api = Blueprint('delete_api', __name__)

from models import *
from web_app import db

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

@delete_api.route('/rooms', methods = ["POST"])
def delete_room():
    data = request.json
    id = data['id']

    room = Rooms.query.filter_by(id=id).first()
    if room is None:
        return 'ERROR ROOM NOT FOUND'
    db.session.delete(room)
    db.session.commit()
    return  "Room %s removed from database" % (room.type)

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

@delete_api.route('/scheduleInitial', methods = ["POST"])
def delete_schedule_initial():
    data = request.json
    id = data['id']

    si = ScheduleInitial.query.filter_by(id=id).first()
    if si is None:
        return 'ERROR SCHEDULE INITIAL NOT FOUND'
    db.session.delete(si)
    db.session.commit()
    return  "Schedule Initial %s removed from database" % (si.term)

@delete_api.route('/publishedSchedule', methods = ["POST"])
def delete_published_schedule():
    data = request.json
    id = data['id']

    ps = PublishedSchedule.query.filter_by(id=id).first()
    if ps is None:
        return 'ERROR PUBLISHED SCHEDULE NOT FOUND'
    db.session.delete(ps)
    db.session.commit()
    return  "Published Schedule %s removed from database" % (ps.term)

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

@delete_api.route('/facultyConstraint', methods = ["POST"])
def delete_faculty_constraint():
    data = request.json
    id = data['id']

    fc = FacultyConstraint.query.filter_by(id=id).first()
    if fc is None:
        return 'ERROR FACULTY CONSTRAINT NOT FOUND'
    db.session.delete(fc)
    db.session.commit()
    return  "Faculty Constraint %s removed from database" % (fc.constraint)

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