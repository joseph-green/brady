from brady import create_app

def test_config():
	assert not create_app().testing 
	assert create_app({"TESTING": True}).testing

def test_index(client):
	response = client.get("/")

	#response returns OK
	assert response.status_code == 200

	#response returns HTML
	assert response.headers.get("Content-Type") == 'text/html; charset=utf-8'
	assert response.data 
