from flask import Blueprint, render_template, flash, redirect, request, url_for, jsonify

#It breaks when you uncomment the line below
#Zach pleaseeee figure this out. 
#from models import *


login_api = Blueprint('login_api', __name__)


@login_api.route('/validateLogin', methods = ["GET"])
def validate_login():
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


# @app.route('/newUser', methods = ["POST"])
# def retrieve_fact():
    
#     fact_id = request.args.get('id', -1, type = int)
#     if fact_id >= 0: #non-invalid id in request
#         fact = models.Fact.query.filter_by(id=fact_id).first()
#         if fact is not None: #results produced
#             return jsonify(id=fact.id,
#                             tags=fact.tags,
#                             quote=fact.quote)
#         else:
#             return 'ERROR RETRIEVING FACT!'
