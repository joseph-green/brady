from flask import Flask, render_template
from flask.ext.cache import Cache
import sqlite3
import json
import os
from . import db


def create_app(test_config=None):

    #initialize app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path,"nfl.db"),
        HAYSTACK_KEY=os.environ["API_KEY"])

    #initialize cache
    cache = Cache(app, {"CACHE_TYPE": "simple"})

    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route('/players/<int:player_id>', methods=['GET'])
    @cache.memoize(timeout=50)
    def get_player_by_id(player_id):

        player = db.get_player_by_id(player_id)
        
        return player


    @app.route('/players/search/<string:player_last_name>', methods=['GET'])
    @cache.memoize(timeout=50)
    def get_player_by_last_name(player_last_name):

        players = db.get_player_by_name(player_last_name.capitalize())
        
        return players


    @app.route('/players/search/<string:player_last_name>/<string:player_first_name>', methods=['GET'])
    @cache.memoize(timeout=50)
    def get_player_by_full_name(player_last_name,player_first_name):

        players = db.get_player_by_name(player_last_name.capitalize(),player_first_name.capitalize())

        return players


    @app.route('/', methods=['GET'])
    @cache.cached(timeout=50)
    def index():
        
        return render_template('index.html')


    return app

