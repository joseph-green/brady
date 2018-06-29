import requests
import json
import base64
import os


def get_attractiveness(image_loc):

	img = open(image_loc, 'rb')

	b64_img = base64.b64encode(img.read())

	req_params = {
	"apiKey": os.environ["API_KEY"],
	"model": "attractiveness",
	"image": b64_img,
	"output": "json"
	}

	response = requests.post("https://api.haystack.ai/api/image/analyze", params = req_params).json()

	attractiveness_score = response["people"][0]["attractiveness"]
	
	return attractiveness_score


