import requests

#get_attractiveness returns the attractiveness of the person contained 
#in the headshot using the Haystack.ai API
#requires: there is only one person in the image
def get_attractiveness(image):

	req_params = {
	"apiKey": "422c39c1be25908f5fbe3861d983f9a6",
	"model": "attractiveness",
	"image": open(image, 'rb'),
	"output": "json"
	}

	response = requests.post("https://api.haystack.ai/api/image/analyze", params = req_params)

	attractiveness_score = response["people"][0]["attractiveness"]

	return attractiveness_score


