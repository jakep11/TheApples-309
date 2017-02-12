from flask import Flask, send_file
from flask_sqlalchemy import SQLAlchemy

from web_app import app

import database.login
import database.filters
import database.create
import database.delete
import database.edit
import database.csvImport
import database.get

app.register_blueprint(database.login.login_api, url_prefix="/users")
app.register_blueprint(database.filters.filters_api, url_prefix="/filter")
app.register_blueprint(database.create.create_api, url_prefix="/create")
app.register_blueprint(database.delete.delete_api, url_prefix="/delete")
app.register_blueprint(database.edit.edit_api, url_prefix="/edit")
app.register_blueprint(database.get.get_api, url_prefix="/get")

app.register_blueprint(database.csvImport.csvImport_api)


@app.route("/")
def index():
    return send_file("static/app/index.html")
	
if __name__ == "__main__":
    app.run(host='0.0.0.0')