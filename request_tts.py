#https://devpost.com/software/wall-eco/

import requests


def speak(text):

	url = "http://localhost:5000/speak"

	requests.get(url, data={"text": text})

