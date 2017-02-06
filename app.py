from flask import Flask, send_file
from flask_sqlalchemy import SQLAlchemy

from web_app import app

import database.login
import database.filters
import database.courses
import database.create
import database.delete
import database.edit

app.register_blueprint(database.login.login_api, url_prefix="/users")
app.register_blueprint(database.filters.filters_api, url_prefix="/view")
app.register_blueprint(database.courses.courses_api, url_prefix="/courses")
app.register_blueprint(database.create.create_api, url_prefix="/create")
app.register_blueprint(database.delete.delete_api, url_prefix="/delete")
app.register_blueprint(database.edit.edit_api, url_prefix="/edit")

@app.route("/")
def index():
    return send_file("static/app/index.html")
	
if __name__ == "__main__":
    app.run(host='0.0.0.0')