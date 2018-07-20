import pytest
import brady
import os

@pytest.fixture
def app():

	#set up environment variables
	os.environ["API_KEY"] = "testkey00000"

	#set up testing configuration
	app = brady.create_app({
		"TESTING": True,
		})

	yield app


@pytest.fixture
def client(app):

	return app.test_client()