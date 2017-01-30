from flask import Flask, send_file

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return send_file("static/app/index.html")
	
if __name__ == "__main__":
    app.run(host='0.0.0.0')

