import requests
from bs4 import BeautifulSoup
import json

def get_fights_from_log_id(log_id):
	r = requests.get("https://www.warcraftlogs.com/reports/fights_and_participants/"+log_id+"/0")
	r = json.loads(r.text)
	return r

def find_boss_fights(r, log_id):
	kills = []
	fights = r["fights"]
	for i in fights:
		if i["boss"] != 0:
			if i["bossPercentage"] == 0:
				boss_dict = {}
				boss_dict["boss_id"] = i["boss"]
				boss_dict["fight_id"] = i["id"]
				boss_dict["boss_name"] = i["name"]
				boss_dict["url"] = "https://www.warcraftlogs.com/rankings/report_rankings_for_fight/"+str(log_id)+"/"+str(boss_dict["fight_id"])+"/"+str(boss_dict["boss_id"])
				kills.append(boss_dict)
	return kills

def scrape_rankings(kills):
	for kill in kills:
		r=requests.get(kill["url"])
		soup = BeautifulSoup(r.text)
		print soup
	pass

def clean_rankings(scraped_stuff):
	pass

def analyze(log_id):
	r = get_fights_from_log_id(log_id)
	kills = find_boss_fights(r, log_id)
	scrape_rankings(kills)
	return kills