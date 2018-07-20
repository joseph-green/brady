import json

def test_player_by_id(client):
	response = client.get("players/228")

	assert response.status_code == 200
	assert response.is_json

	assert response.data == bytes('{"player_id": 228, "player_first_name": "Tom", "player_last_name": "Brady", "player_position": "QB", "player_team": "New England Patriots", "player_attractiveness": 7.4254}','utf-8')

def test_player_search_by_last_name(client):
	response = client.get("players/search/gronkowski")

	assert response.status_code == 200
	assert response.is_json

	assert response.data == bytes('[{"player_id": 850, "player_first_name": "Glenn", "player_last_name": "Gronkowski", "player_position": "FB", "player_team": "Buffalo Bills", "player_attractiveness": 6.4971}, {"player_id": 851, "player_first_name": "Rob", "player_last_name": "Gronkowski", "player_position": "TE", "player_team": "New England Patriots", "player_attractiveness": 6.4279}]','utf-8')

def test_player_search_by_full_name(client):
	response = client.get("players/search/gronkowski/rob")

	assert response.status_code == 200
	assert response.is_json

	assert response.data == bytes('[{"player_id": 851, "player_first_name": "Rob", "player_last_name": "Gronkowski", "player_position": "TE", "player_team": "New England Patriots", "player_attractiveness": 6.4279}]','utf-8')

