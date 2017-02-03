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
    uname = request.args.get('username') 
    print 'yo'
    print uname
    print 'hi'
    print 'hi'
    user = User.query.filter_by(username=uname).first()
    isUser = True
    if user is None:
        isUser = False
    return jsonify(isUser=isUser)
    #return jsonify(id=1, role='chair', username='jake')

    # tree_id = request.args.get('id', -1, type = int)
    # if tree_id >= 0: #non-invalid id in request
    #     tree = models.Tree.query.filter_by(id=tree_id).first()
    #     if tree is not None: #results produced
    #         return jsonify(id=tree.id,
    #                         topic=tree.topic,
    #                         user=tree.user.username)
    #     else:
    #         return 'ERROR RETRIEVING TREE!'


@login_api.route('/createUser', methods = ["POST"])
def retrieve_fact():
    data = request.json
    
    

    username = data['username']
    print data  
    print username
    print "!!!!!username!!!!"        
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    role = data['role']

    hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    #hashed = password

    newUser = User(username=username, password_hash=hashed, first_name=first_name, last_name=last_name, role=role)
    db.session.add(newUser)
    db.session.commit()
    return "success"
    
