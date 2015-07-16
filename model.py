import requests
from bs4 import BeautifulSoup
import json

def get_fights_from_log_id(log_id):
	r = requests.get("https://www.warcraftlogs.com/reports/fights_and_participants/"+log_id+"/0")
	r = json.loads(r.text)
	return r

def find_boss_fights(r):
	kills = []
	fights = r["fights"]
	for i in fights:
		if i["boss"] != 0:
			if i["bossPercentage"] == 0:
				boss_dict = {}
				boss_dict["boss_id"] = i["boss"]
				boss_dict["fight_id"] = i["id"]
				boss_dict["boss_name"] = i["name"]
				kills.append(boss_dict)
	return kills


def create_urls_from_kills(kill_list):
	pass

def scrape_rankings(url_list):
	pass

def clean_rankings(scraped_stuff):
	pass

def analyze(log_id):
	r = get_fights_from_log_id(log_id)
	kills = find_boss_fights(r)
	return kills