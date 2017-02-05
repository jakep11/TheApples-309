from flask import Blueprint, render_template, flash, redirect, request, url_for, jsonify, json

courses_api = Blueprint('courses_api', __name__)

from models import *
from web_app import db

@courses_api.route('/allCourses', methods = ["GET"])
def get_courses():
	courses = Courses.query.all()
	return jsonify([i.serialize for i in courses])
