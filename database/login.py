from flask import Blueprint, render_template, flash, redirect, request, url_for, jsonify, json
import bcrypt
login_api = Blueprint('login_api', __name__)

from models import *
from web_app import db

@login_api.route('/allUsers', methods = ["GET"])
def sample_function():
    users = User.query.all()
    return jsonify([i.serialize for i in users])


@login_api.route('/validateLogin', methods = ["POST"])
def validate_login2():
    data = request.json
    username = data['username']
    password = data['password']

    #Retrieve User with specified username from the database
    user = User.query.filter_by(username=username).first()

    isUser = True
    role = None
    first_name = None
    last_name = None
    if user is None: #if username not in database
        isUser = False
    #username exists
    elif bcrypt.hashpw(password.encode('utf8'), user.password_hash.encode('utf8')) == user.password_hash.encode('utf8'):
        #Password matches
        isUser = True
        role = user.role
        first_name = user.first_name
        last_name = user.last_name

    return jsonify(isUser=isUser, role=role, first_name=first_name, last_name=last_name)
    


@login_api.route('/createUser', methods = ["POST"])
def retrieve_fact():
    data = request.json

    username = data['username']     
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    role = data['role']

    hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

    newUser = User(username=username, password_hash=hashed, first_name=first_name, last_name=last_name, role=role)
    db.session.add(newUser)
    db.session.commit()
    return "success"
    
