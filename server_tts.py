#https://devpost.com/software/wall-eco/
from flask import Flask, request, jsonify
from gtts import gTTS
from playsound import playsound
import os

app = Flask(__name__)

def say(text):
	tts = gTTS(text)
	tts.save(os.path.dirname(os.path.realpath(__file__)) + "text.mp3")
	playsound(os.path.dirname(os.path.realpath(__file__)) + "text.mp3")
	os.remove(os.path.dirname(os.path.realpath(__file__)) + "text.mp3")


@app.route("/speak")
def speak():
	text = request.values.get("text")
	say(text)
	return jsonify({"status": True})

if __name__ == "__main__":
	app.run()

