import sqlite3
import json

def db_connect():
    db_conn = sqlite3.connect('./nfl.db')
    db = db_conn.cursor()

    return db

def db_close(db_conn):
    
    #close the database
    db_conn.close()

def get_player_by_id(player_id):

    db = db_connect()

    db.execute("""SELECT player_id, player_first_name, player_last_name, player_position, player_team FROM players WHERE player_id=?""", (player_id,))

    player = db.fetchone()

    keys = [des[0] for des in db.description]

    db_close(db)

    if player:
        response_hash = parse_player(player,keys)
        return json.dumps(response_hash)
    else:
    	return "No results were found"

def get_player_by_name(last_name,first_name=None):

    db = db_connect()
    
    #if a first name is given, search using first and last names, otherwise just by last name
    if first_name:
        db.execute("""SELECT player_id, player_first_name, player_last_name, player_position, player_team FROM players WHERE player_first_name=? AND player_last_name=?""", (first_name,last_name))
    else:
        db.execute("""SELECT player_id, player_first_name, player_last_name, player_position, player_team FROM players WHERE player_last_name=?""", (last_name,))

    players = db.fetchall()

    keys = [des[0] for des in db.description]

    db_close(db)

    #if no players are found, return an error
    if len(players) == 0:
        return "No results were found"
    else:
        
        players_reponse_hash = [parse_player(player,keys) for player in players]

        return json.dumps(players_reponse_hash)
    

    



def parse_player(response,columns):

    response_hash = {}

    for i in range(0,len(response)):
        response_hash[columns[i]] = response[i]

    return response_hash

