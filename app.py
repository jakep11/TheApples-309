from flask import Flask, send_file
from flask_sqlalchemy import SQLAlchemy

from web_app import app

import database.login

app.register_blueprint(database.login.login_api, url_prefix="/users")
app.register_blueprint(database.create.create_api, url_prefix="/create")

@app.route("/")
def index():
    return send_file("static/app/index.html")
	
if __name__ == "__main__":
    app.run(host='0.0.0.0')