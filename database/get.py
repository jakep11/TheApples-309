from flask import Blueprint, render_template, flash, redirect, request, url_for, jsonify, json

get_api = Blueprint('get_api', __name__)

from models import *
from web_app import db

@get_api.route('/terms', methods = ["GET"])
def get_terms():
	terms = Terms.query.all()
	return jsonify([i.serialize for i in terms])