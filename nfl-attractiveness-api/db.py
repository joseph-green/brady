import sqlite3

def db_connect():
    db_conn = sqlite3.connect('./nfl.db')
    db = db_conn.cursor()

    return db

def db_close(db_conn):
    
    #close the database
    db_conn.close()

def get_player_by_id(player_id):

    db = db_connect()

    db.execute("""SELECT * FROM players WHERE player_id=?""", (player_id,))

    player = db.fetchone()

    return player

    db_close(db)

def get_player_by_name(last_name,first_name=None):

    db = db_connect()
    
    #if a first name is given, search using first and last names, otherwise just by last name
    if first_name:
        db.execute("""SELECT * FROM players WHERE player_first_name=? AND player_last_name=?""", (first_name,last_name))
    else:
        db.execute("""SELECT * FROM players WHERE player_last_name=?""", (last_name,))

    players = db.fetchall()

    #if no players are found, return an error
    if len(players) == 0:
        return "No results were found"
    #if a single player is found, return that player
    elif len(players) == 1:
        return players[0]
    else:
        return players
    

    db_close(db)


