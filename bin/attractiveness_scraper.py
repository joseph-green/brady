import attractiveness_rater
import sqlite3
import re
import os.path


def update_attractiveness():

	#initialize the database connection and set the cursor
	db_conn = sqlite3.connect('../nfl.db')
	db = db_conn.cursor()

	i = 1

	while (1):

		db.execute("""SELECT img_path, player_attractiveness FROM players WHERE player_id=?""", (i,))

		player = db.fetchone()

		#if the player exists and does not have an attractiveness rating, update
		if player and not player[1]:

			img = player[0]

			if img:
				
				attractiveness = attractiveness_rater.get_attractiveness(img)

				if attractiveness and attractiveness < 0:
					break

				db.execute("""UPDATE players SET player_attractiveness=? WHERE player_id=?""", (attractiveness,i))

		i += 1

	#commit and close the database
	db_conn.commit()
	db_conn.close()

def update_attractiveness_by_file():

	#initialize the database connection and set the cursor
	db_conn = sqlite3.connect('../nfl.db')
	db = db_conn.cursor()

	i = 1

	while (1):

		db.execute("""SELECT img_path, player_attractiveness FROM players WHERE player_id=?""", (i,))

		player = db.fetchone()

		afile = open("../player_attractiveness.txt", 'r')

		values = re.findall(r"(?<='attractiveness': )\d\.\d+",afile.read())

		#if the player exists and does not have an attractiveness rating, update
		if player and not player[1]:

			img = player[0]

			if os.path.isfile(img):

				try:

					attractiveness = values[i-1]
				except IndexError: 
					break


				db.execute("""UPDATE players SET player_attractiveness=? WHERE player_id=?""", (attractiveness,i))

		i += 1

	#commit and close the database
	db_conn.commit()
	db_conn.close()

