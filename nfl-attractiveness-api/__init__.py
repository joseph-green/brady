from flask import Flask
import sqlite3
import json
import os
from db import get_player_by_id, get_player_by_name


def setup_api():
	app = Flask(__name__, instance_relative_config=True)

	app.config.from_mapping(
		SECRET_KEY="dev",
		DATABASE=os.path.join(app.instance_path,"nfl.db"),
		HAYSTACK_KEY=os.environ["API_KEY"])

	if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


	@app.route('/players/<string:player_id>', methods=['GET'])
	def get_player_by_id(player_id):

	    player = get_player_by_id(player_id)

	    response = json.dumps(player)

	    db_close(db)
		
	    return response

	return app