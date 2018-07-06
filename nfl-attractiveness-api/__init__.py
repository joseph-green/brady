from flask import Flask
import sqlite3
import json
import os
from . import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    print(app.instance_path)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path,"nfl.db"),
            HAYSTACK_KEY=os.environ["API_KEY"])

    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route('/players/<int:player_id>', methods=['GET'])
    def get_player_by_id(player_id):

        player = db.get_player_by_id(player_id)

        response = json.dumps(player)
        
        return response

    @app.route('/players/search/<string:player_last_name>', methods=['GET'])
    def get_player_by_last_name(player_last_name):

        player = db.get_player_by_name(player_last_name)

        response = json.dumps(player)
        
        return response

    @app.route('/players/search/<string:player_last_name>/<string:player_first_name>', methods=['GET'])
    def get_player_by_full_name(player_last_name,player_first_name):

        player = db.get_player_by_name(player_last_name,player_first_name)

        response = json.dumps(player)
        
        return response


    return app

