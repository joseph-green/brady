from flask import Flask, render_template, Response
from flask_caching import Cache
import sqlite3
import json
import os
from . import error
from . import db


def create_app(test_config=None):



    #initialize app
    app = Flask(__name__, instance_relative_config=True)



    #set default config
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path,"nfl.db"),
        HAYSTACK_KEY=os.environ["API_KEY"],
        TESTING=False)



    #initialize cache
    cache = Cache(app, {"CACHE_TYPE": "simple"})



    #set config
    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass




    #display docs page at index
    @app.route('/', methods=['GET'])
    @cache.cached(timeout=50)
    def index():
        
        return render_template('index.html')




    #get players by their unique player ID
    @app.route('/players/<int:player_id>', methods=['GET'])
    @cache.memoize(timeout=50)
    def get_player_by_id(player_id):   

        try:
            player = db.get_player_by_id(player_id)
        except error.Exception as e:
            return Response(e.message, status=e.status_code)

        return Response(player,content_type='application/json')





    #search for players by last name only
    @app.route('/players/search/<string:player_last_name>', methods=['GET'])
    @cache.memoize(timeout=50)
    def get_player_by_last_name(player_last_name):

        
        
        try:
            players = db.get_player_by_name(player_last_name.capitalize())
        except error.Exception as e:
            return Response(e.message, status=e.status_code)

        return Response(players,content_type='application/json')





    #search for players by first and last name
    @app.route('/players/search/<string:player_last_name>/<string:player_first_name>', methods=['GET'])
    @cache.memoize(timeout=50)
    def get_player_by_full_name(player_last_name,player_first_name):

        

        try:
            players = db.get_player_by_name(player_last_name.capitalize(),player_first_name.capitalize())  
        except Exception as e:
            return Response(e.message, status=e.status_code)

        return Response(players,content_type='application/json')



    return app

