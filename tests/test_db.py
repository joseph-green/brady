import sqlite3
from brady.db import *



def test_get_by_id():

	results = get_player_by_id(228)

	assert type(results) == str

	assert results == '{"player_id": 228, "player_first_name": "Tom", "player_last_name": "Brady", "player_position": "QB", "player_team": "New England Patriots", "player_attractiveness": 7.4254}'



def test_search_last_name():

	results = get_player_by_name("Gronkowski")

	assert type(results) == str

	assert results == '[{"player_id": 850, "player_first_name": "Glenn", "player_last_name": "Gronkowski", "player_position": "FB", "player_team": "Buffalo Bills", "player_attractiveness": 6.4971}, {"player_id": 851, "player_first_name": "Rob", "player_last_name": "Gronkowski", "player_position": "TE", "player_team": "New England Patriots", "player_attractiveness": 6.4279}]'


def test_search_full_name():

	results = get_player_by_name("Gronkowski","Rob")

	assert type(results) == str

	assert results == '[{"player_id": 851, "player_first_name": "Rob", "player_last_name": "Gronkowski", "player_position": "TE", "player_team": "New England Patriots", "player_attractiveness": 6.4279}]'
