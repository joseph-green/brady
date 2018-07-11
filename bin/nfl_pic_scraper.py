import requests
import re
import urllib.request
import attractiveness_rater
import sqlite3



BASE_URL = "https://www.pro-football-reference.com"



def get_file_location(player_first_name,player_last_name,player_position):
    if not player_position:
        return '../assets/player_headshots/' + player_first_name + "_" + player_last_name + '.jpg'
    else:
        return '../assets/player_headshots/' + player_position + "_" + player_first_name + "_" + player_last_name + '.jpg'



def scrape_player_img(player_url, file_location):

    #get the html content from the page
    html_response = requests.get(player_url).text

    #get the image location
    img_location = re.search(r"https://d395i9ljze9h3x.cloudfront.net/.+?.jpg", html_response)

    #if the player has an image on their page 
    if img_location != None:
        img_location = img_location.group(0)
        urllib.request.urlretrieve(img_location, file_location)

        #initialize attractiveness variable to be changed by scraping function
        global player_attractiveness

        #get player attractivness
        player_attractiveness = attractiveness_rater.get_attractiveness(file_location)

    


def get_player_team(player_url):

    #get the body from the player profile
    html_response = requests.get(player_url).text

    #find the team in the body via regex
    player_team = re.search(r'<a href="/teams/.+">.+</a>',html_response).group(0)
    player_team = re.search(r"[A-Z]{1}[A-Za-z ]+",player_team).group(0)

    return player_team


def scrape_index(last_initial):

    #generate the url for the index
    index_url = BASE_URL + '/players/' + last_initial

    #get the html body from PFR
    html_response = requests.get(index_url).text

    #get the list of players
    html_body = re.search(r'<div class="section_content" id="div_players">(.|\n)+?</div>',html_response).group(0);

    #find all active players (which are in bold)
    active_players = re.findall(r'<b>.+?</b>',html_body)
    
    #create the table
    db.execute('''CREATE TABLE IF NOT EXISTS players (
        player_id INTEGER PRIMARY KEY, 
        player_first_name varchar(100) NOT NULL,
        player_last_name varchar(100) NOT NULL,
        player_position char(10),
        player_team char(100),
        player_attractiveness real,
        img_path text)''')

    for player in active_players:

        #get player first and last name
        player_name = re.search(r"[A-Z]{1}[A-Za-z\.'-]+ [A-Z]{1}[A-Za-z\.'-]+",player).group(0).split(" ")
        player_first_name = player_name[0]
        player_last_name = player_name[1]

        #get player position
        player_position = re.search(r'\([A-Z]+\)',player)

        #if a position is found, perform the second search
        if player_position != None:
            player_position = re.search(r'[A-Z]+',player_position.group(0)).group(0)

        #find the unique url extension for the player and generate url
        player_extension = re.search(r'/players/.+\.htm',player).group(0);
        player_url = BASE_URL + player_extension

        #get the player's team from their profile
        player_team = get_player_team(player_url)



        #generate a location for the player's image
        file_location = get_file_location(player_first_name, player_last_name, player_position)


        

        #scrape the player's headshot from their profile
        scrape_player_img(player_url,file_location)


        #insert information into table
        db.execute("""INSERT INTO 
            players (player_first_name,player_last_name,player_position,player_team,img_path) 
            VALUES (?,?,?,?,?)""", (player_first_name,player_last_name,player_position,player_team,file_location))

        





#initialize the database connection and set the cursor
db_conn = sqlite3.connect('../brady/nfl.db')
db = db_conn.cursor()

#perform an index scrape on all last initials
for index in range(ord("A"),ord("Z") + 1):
    print("Scraping " + chr(index) + "...")
    scrape_index(chr(index))

#commit and close the database
db_conn.commit()
db_conn.close()