from flask import Blueprint, render_template, flash, redirect, request, url_for, jsonify, json

get_api = Blueprint('get_api', __name__)

from models import *
from web_app import db

@get_api.route('/terms', methods = ["GET"])
def get_terms():
	terms = Terms.query.all()
	return jsonify([i.serialize for i in terms])

@get_api.route('/instructors', methods = ["GET"])
def get_instructors():
	instructors = Faculty.query.all()
	return jsonify([i.serialize for i in instructors])

@get_api.route('/sections', methods = ["GET"])
def get_sections():
	sections = Sections.query.all()
	return jsonify([i.serialize for i in sections])