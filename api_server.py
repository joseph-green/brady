from flask import Flask
import sqlite3
import json

app = Flask(__name__)



@app.route('/players/<string:player_id>', methods=['GET'])
def get_player_by_id(player_id):
    db_conn = sqlite3.connect('nfl.db')
    db = db_conn.cursor()
    db.execute("""SELECT * FROM players WHERE player_last_name=?""", (player_id,))
    player = db.fetchall()

    response = json.dumps(player)

    #close the database
	db_conn.close()
	
    return response