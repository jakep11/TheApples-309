from flask import Blueprint, render_template, flash, redirect, request, url_for, jsonify

login_api = Blueprint('login_api', __name__)

from models import *
from web_app import db

@login_api.route('/testApiEndpoint', methods = ["GET"])
def sample_function():
    #user = User.query.filter_by(username=username).first_or_404()
    #return user
    return jsonify(id=1, role='chair', username='jake')

    # tree_id = request.args.get('id', -1, type = int)
    # if tree_id >= 0: #non-invalid id in request
    #     tree = models.Tree.query.filter_by(id=tree_id).first()
    #     if tree is not None: #results produced
    #         return jsonify(id=tree.id,
    #                         topic=tree.topic,
    #                         user=tree.user.username)
    #     else:
    #         return 'ERROR RETRIEVING TREE!'

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


@login_api.route('/newUser', methods = ["POST"])
def retrieve_fact():
    
    username = request.args.get('username')
    password = request.args.get('password')
    print username, password
    newUser = User(username=username, password=password)
    db.session.add(newUser)
    db.session.commit()
    return newUser
    # fact_id = request.args.get('id', -1, type = int)
    # if fact_id >= 0: #non-invalid id in request
    #     fact = models.Fact.query.filter_by(id=fact_id).first()
    #     if fact is not None: #results produced
    #         return jsonify(id=fact.id,
    #                         tags=fact.tags,
    #                         quote=fact.quote)
    #     else:
    #         return 'ERROR RETRIEVING FACT!'
