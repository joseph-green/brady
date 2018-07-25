import sqlite3
import json
from brady.error import Exception



def db_connect():
    db_conn = sqlite3.connect('./nfl.db')
    db = db_conn.cursor()

    return db



def db_close(db_conn):
    
    #close the database
    db_conn.close()



def get_player_by_id(player_id):

    db = db_connect()

    #find all players with given id
    db.execute("""SELECT player_id, player_first_name, player_last_name, player_position, player_team, player_attractiveness FROM players WHERE player_id=?""", (player_id,))

    player = db.fetchone()

    #fetch all the database headers
    keys = [des[0] for des in db.description]

    db_close(db)

    #if a player is found, return the result in json, otherwise return an error
    if player:
        response_hash = parse_player(player,keys)
        return json.dumps(response_hash)
    else:
    	raise Exception(404,"No results were found")



def get_player_by_name(last_name,first_name=None):

    db = db_connect()
    
    #if a first name is given, search using first and last names, otherwise just by last name
    if first_name:
        db.execute("""SELECT player_id, player_first_name, player_last_name, player_position, player_team, player_attractiveness FROM players WHERE player_first_name=? AND player_last_name=?""", (first_name,last_name))
    else:
        db.execute("""SELECT player_id, player_first_name, player_last_name, player_position, player_team, player_attractiveness FROM players WHERE player_last_name=?""", (last_name,))

    players = db.fetchall()

    #fetch database headers
    keys = [des[0] for des in db.description]

    db_close(db)

    #if no players are found, return an error
    #otherwise, return a json list of all players 
    if len(players) == 0:
        raise Exception(404,"No results were found")
    else:        
        players_reponse_hash = [parse_player(player,keys) for player in players]
        return json.dumps(players_reponse_hash)
    



def parse_player(response,columns):

    response_hash = {}

    #map all keys (i.e. database headers) to appropriate values
    for i in range(0,len(response)):
        response_hash[columns[i]] = response[i]

    return response_hash

