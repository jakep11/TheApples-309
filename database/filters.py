from flask import Blueprint, render_template, flash, redirect, request, url_for, jsonify, json

filters_api = Blueprint('filters_api', __name__)

from models import *
from web_app import db

# grab all courses
@filters_api.route('/allCourses', methods=["GET"])
def all_courses():
    courses = Courses.query.all()
    return jsonify([i.serialize for i in courses])


@filters_api.route('/filteredCourses', methods=["GET"])
def filtered_courses():
    courses = Courses.query.all()
    return jsonify([i.serialize for i in courses])


# grab all sections
@filters_api.route('/allSections', methods=["GET"])
def all_sections():
    sections = Sections.query.all()
    return jsonify([i.serialize for i in sections])
