#https://devpost.com/software/wall-eco/
from flask import Flask, request, url_for, send_from_directory, jsonify
import os

app = Flask(__name__)

@app.route("/upload")
def upload():
	img = request.files.get("image")
	img.save(os.path.join("images", img.filename))

	return jsonify({'url' : request.url_root[:-1] + url_for("get_image", name=img.filename)})



@app.route("/image/<name>")
def get_image(name):
	return send_from_directory(os.path.join("images"), name)

if __name__ == "__main__":
	app.run()
