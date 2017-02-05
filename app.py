from flask import Flask, send_file
from flask_sqlalchemy import SQLAlchemy

from web_app import app

import database.login
import database.filters

app.register_blueprint(database.login.login_api, url_prefix="/users")
app.register_blueprint(database.filters.filters_api, url_prefix="/view")

@app.route("/")
def index():
    return send_file("static/app/index.html")
	
if __name__ == "__main__":
    app.run(host='0.0.0.0')