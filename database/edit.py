from flask import Blueprint, request, jsonify, json
edit_api = Blueprint('edit_api', __name__)

from models import *
from web_app import db

@edit_api.route('/user', methods = ["POST"])
def edit_user():
    data = request.json
    id = data['id']
    username = data['username']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']

    user = User.query.filter_by(id=id).first()
    if user is None:
        return 'ERROR USER NOT FOUND'
    if username is not None:
    	user.username = username
    if password is not None:
    	user.password = password
    if first_name is not None:
    	user.first_name = first_name
    if last_name is not None:
    	user.last_name = last_name

    db.session.add(user)
    db.session.commit()
    # Re-set user variable to reflect any changes
    user = User.query.filter_by(id=id).first()
    return  "User %s updated" (user.username)