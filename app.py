from flask import Flask, send_file
from flask_sqlalchemy import SQLAlchemy
import database.login


app = Flask(__name__)
app.register_blueprint(database.login.login_api)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://db:password@35.160.55.128/cs2scheduling'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    return send_file("static/app/index.html")
	
if __name__ == "__main__":
    app.run(host='0.0.0.0')