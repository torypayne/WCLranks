import requests
from bs4 import BeautifulSoup
import json
import re

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
	rankings = {}
	for kill in kills:
		r=requests.get(kill["url"])
		soup = BeautifulSoup(r.text, "html5lib")
		data = dps_rankings(soup, rankings, kill["boss_name"])
	return data

def dps_rankings(soup, rankings, boss_name):
	table = soup.findAll("table")[3]
	for row in table.findAll("tr")[1:]:
		link = row.findAll("a")[0]
		name = link.contents[0]
		spec_path = row.findAll("img")[0]["src"]
		spec = re.findall( '-(.*?).jpg', spec_path)[0]
		if name not in rankings:
			rankings[name] = {}
			rankings[name]["class"] = link['class']
			rankings[name]["spec_path"] = spec_path
			rankings[name]["spec"] = spec
		rankings[name][boss_name] = {}
		rankings[name][boss_name]["rank"] = row.findAll("td")[0].contents[0]
		rankings[name][boss_name]["spec"] = spec
		rankings[name][boss_name]["damage"] = row.findAll("td")[5].contents[0]
		rankings[name][boss_name]["ilvl"] = row.findAll("td")[6].contents[0]
		rankings[name][boss_name]["bracket"] = row.findAll("td")[7].contents[0]
		rankings[name][boss_name]["br_rank"] = row.findAll("td")[8].contents[0]
	return rankings


def analyze(log_id):
	r = get_fights_from_log_id(log_id)
	kills = find_boss_fights(r, log_id)
	details = scrape_rankings(kills)
	return kills, details