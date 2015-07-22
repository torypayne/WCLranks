import requests
from bs4 import BeautifulSoup
import json
import re
import redis
import time
import datetime

try:
	r = redis.from_url(os.environ.get('REDIS_URL'))
except:
	pass
	# import config
	# r = redis.from_url(config.REDIS_URL)

def get_fights_from_log_id(log_id):
	r = requests.get("https://www.warcraftlogs.com/reports/fights_and_participants/"+log_id+"/0")
	r = json.loads(r.text)
	return r

def find_boss_fights(r, log_id):
	kills = []
	fights = r["fights"]
	for i in fights:
		if i["boss"] != 0:
			if i["kill"] == True:
				boss_dict = {}
				boss_dict["boss_id"] = i["boss"]
				boss_dict["fight_id"] = i["id"]
				boss_dict["boss_name"] = i["name"]
				boss_dict["url"] = "https://www.warcraftlogs.com/rankings/report_rankings_for_fight/"+str(log_id)+"/"+str(boss_dict["fight_id"])+"/"+str(boss_dict["boss_id"])
				kills.append(boss_dict)
	return kills

def scrape_rankings(kills):
	rankings = {}
	non_kill = []
	rankings["tank"] = {}
	rankings["dps"] = {}
	rankings["hps"] = {}
	rankings["guild"] = {}
	rankings["guild"]["execution"] = {}
	rankings["guild"]["execution"]["rank"] = {}
	rankings["guild"]["execution"]["rank_class"] = {}
	rankings["guild"]["execution"]["deaths"] = {}
	rankings["guild"]["execution"]["damage_taken"] = {}
	rankings["guild"]["speed"] = {}
	rankings["guild"]["speed"]["rank"] = {}
	rankings["guild"]["speed"]["rank_class"] = {}
	rankings["guild"]["speed"]["duration"] = {}
	for kill in kills:
		r=requests.get(kill["url"])
		print kill["url"]
		soup = BeautifulSoup(r.text, "html5lib")
		data = dps_rankings(soup, rankings, kill["boss_id"])
		data = hps_rankings(soup, rankings, kill["boss_id"])
		data = tank_rankings(soup, rankings, kill["boss_id"])
		data = guild_rankings(soup, rankings, kill["boss_id"])
	return data

def dps_rankings(soup, rankings, boss_id):
	table = soup.findAll("table")[3]
	for row in table.findAll("tr")[1:]:
		link = row.findAll("a")[0]
		name = link.contents[0]
		spec_path = row.findAll("img")[0]["src"]
		spec = re.findall( '-(.*?).jpg', spec_path)[0]
		if name not in rankings["dps"]:
			rankings["dps"][name] = {}
			rankings["dps"][name]["class"] = link['class'][0]
			if rankings["dps"][name]["class"] == "DeathKnight":
				rankings["dps"][name]["class"] = "Death Knight"
			rankings["dps"][name]["spec_path"] = spec_path
			rankings["dps"][name]["spec"] = spec
			rankings["dps"][name]["rank"] = {}
			rankings["dps"][name]["rank_class"] = {}
			rankings["dps"][name]["damage"] = {}
			bracket = row.findAll("td")[7].contents[0]
			bracket = bracket.strip(" Item Level")
			rankings["dps"][name]["bracket"] = bracket
			rankings["dps"][name]["br_rank"] = {}
			rankings["dps"][name]["br_rank_class"] = {}
			rankings["dps"][name]["ilvl"] = row.findAll("td")[6].contents[0]
		rankings["dps"][name]["rank"][boss_id] = row.findAll("td")[0].contents[0]
		x = int(rankings["dps"][name]["rank"][boss_id])
		if x > 50:
			if x > 75:
				if x > 95:
					rankings["dps"][name]["rank_class"][boss_id] = "legendary"
				else:
					rankings["dps"][name]["rank_class"][boss_id] = "epic"
			else:
				rankings["dps"][name]["rank_class"][boss_id] = "rare"
		elif x > 25:
			rankings["dps"][name]["rank_class"][boss_id] = "uncommon"
		else:
			rankings["dps"][name]["rank_class"][boss_id] = "common"
		rankings["dps"][name]["damage"][boss_id] = row.findAll("td")[5].contents[0]
		rankings["dps"][name]["br_rank"][boss_id] = row.findAll("td")[8].contents[0]
		x = int(rankings["dps"][name]["br_rank"][boss_id])
		if x > 50:
			if x > 75:
				if x > 95:
					rankings["dps"][name]["br_rank_class"][boss_id] = "legendary"
				else:
					rankings["dps"][name]["br_rank_class"][boss_id] = "epic"
			else:
				rankings["dps"][name]["br_rank_class"][boss_id] = "rare"
		elif x > 25:
			rankings["dps"][name]["br_rank_class"][boss_id] = "uncommon"
		else:
			rankings["dps"][name]["br_rank_class"][boss_id] = "common"
		if rankings["dps"][name]["spec"] != spec:
			rankings["dps"][name]["spec"] = "Multiple"
	return rankings


def hps_rankings(soup, rankings, boss_id):
	table = soup.findAll("table")[4]
	for row in table.findAll("tr")[1:]:
		link = row.findAll("a")[0]
		name = link.contents[0]
		spec_path = row.findAll("img")[0]["src"]
		spec = re.findall( '-(.*?).jpg', spec_path)[0]
		if name not in rankings["hps"]:
			rankings["hps"][name] = {}
			rankings["hps"][name]["class"] = link['class'][0]
			rankings["hps"][name]["spec_path"] = spec_path
			rankings["hps"][name]["spec"] = spec
			rankings["hps"][name]["rank"] = {}
			rankings["hps"][name]["rank_class"] = {}
			rankings["hps"][name]["healing"] = {}
			bracket = row.findAll("td")[7].contents[0]
			bracket = bracket.strip(" Item Level")
			rankings["hps"][name]["bracket"] = bracket
			rankings["hps"][name]["br_rank"] = {}
			rankings["hps"][name]["br_rank_class"] = {}
			rankings["hps"][name]["ilvl"] = row.findAll("td")[6].contents[0]
		rankings["hps"][name]["rank"][boss_id] = row.findAll("td")[0].contents[0]
		x = int(rankings["hps"][name]["rank"][boss_id])
		if x > 50:
			if x > 75:
				if x > 95:
					rankings["hps"][name]["rank_class"][boss_id] = "legendary"
				else:
					rankings["hps"][name]["rank_class"][boss_id] = "epic"
			else:
				rankings["hps"][name]["rank_class"][boss_id] = "rare"
		elif x > 25:
			rankings["hps"][name]["rank_class"][boss_id] = "uncommon"
		else:
			rankings["hps"][name]["rank_class"][boss_id] = "common"
		rankings["hps"][name]["healing"][boss_id] = row.findAll("td")[5].contents[0]
		rankings["hps"][name]["br_rank"][boss_id] = row.findAll("td")[8].contents[0]
		x = int(rankings["hps"][name]["br_rank"][boss_id])
		if x > 50:
			if x > 75:
				if x > 95:
					rankings["hps"][name]["br_rank_class"][boss_id] = "legendary"
				else:
					rankings["hps"][name]["br_rank_class"][boss_id] = "epic"
			else:
				rankings["hps"][name]["br_rank_class"][boss_id] = "rare"
		elif x > 25:
			rankings["hps"][name]["br_rank_class"][boss_id] = "uncommon"
		else:
			rankings["hps"][name]["br_rank_class"][boss_id] = "common"
		if rankings["hps"][name]["spec"] != spec:
			rankings["hps"][name]["spec"] = "Multiple"
	return rankings

def tank_rankings(soup, rankings, boss_id):
	table = soup.findAll("table")[2]
	for row in table.findAll("tr")[1:]:
		link = row.findAll("a")[0]
		name = link.contents[0]
		spec_path = row.findAll("img")[0]["src"]
		spec = re.findall( '-(.*?).jpg', spec_path)[0]
		if name not in rankings["tank"]:
			rankings["tank"][name] = {}
			rankings["tank"][name]["class"] = link['class'][0]
			if rankings["tank"][name]["class"] == "DeathKnight":
				rankings["tank"][name]["class"] = "Death Knight"
			rankings["tank"][name]["spec_path"] = spec_path
			rankings["tank"][name]["spec"] = spec
			rankings["tank"][name]["rank"] = {}
			rankings["tank"][name]["rank_class"] = {}
			rankings["tank"][name]["healing"] = {}
			bracket = row.findAll("td")[7].contents[0]
			bracket = bracket.strip(" Item Level")
			rankings["tank"][name]["bracket"] = bracket
			rankings["tank"][name]["br_rank"] = {}
			rankings["tank"][name]["br_rank_class"] = {}
			rankings["tank"][name]["ilvl"] = row.findAll("td")[6].contents[0]
		rankings["tank"][name]["rank"][boss_id] = row.findAll("td")[0].contents[0]
		x = int(rankings["tank"][name]["rank"][boss_id])
		if x > 50:
			if x > 75:
				if x > 95:
					rankings["tank"][name]["rank_class"][boss_id] = "legendary"
				else:
					rankings["tank"][name]["rank_class"][boss_id] = "epic"
			else:
				rankings["tank"][name]["rank_class"][boss_id] = "rare"
		elif x > 25:
			rankings["tank"][name]["rank_class"][boss_id] = "uncommon"
		else:
			rankings["tank"][name]["rank_class"][boss_id] = "common"
		rankings["tank"][name]["healing"][boss_id] = row.findAll("td")[5].contents[0]
		rankings["tank"][name]["br_rank"][boss_id] = row.findAll("td")[8].contents[0]
		x = int(rankings["tank"][name]["br_rank"][boss_id])
		if x > 50:
			if x > 75:
				if x > 95:
					rankings["tank"][name]["br_rank_class"][boss_id] = "legendary"
				else:
					rankings["tank"][name]["br_rank_class"][boss_id] = "epic"
			else:
				rankings["tank"][name]["br_rank_class"][boss_id] = "rare"
		elif x > 25:
			rankings["tank"][name]["br_rank_class"][boss_id] = "uncommon"
		else:
			rankings["tank"][name]["br_rank_class"][boss_id] = "common"
		if rankings["tank"][name]["spec"] != spec:
			rankings["tank"][name]["spec"] = "Multiple"
	return rankings

def guild_rankings(soup, rankings, boss_id):
	table = soup.findAll("table")[0]
	for row in table.findAll("tr")[1:]:
		rankings["guild_name"] = row.findAll("td")[4].contents[0]
		rankings["guild_ilvl"] = row.findAll("td")[7].contents[0]
		rankings["guild"]["execution"]["rank"][boss_id] = row.findAll("td")[0].contents[0]
		try:
			x = int(rankings["guild"]["execution"]["rank"][boss_id])
			if x > 50:
				if x > 75:
					if x > 95:
						rankings["guild"]["execution"]["rank_class"][boss_id] = "legendary"
					else:
						rankings["guild"]["execution"]["rank_class"][boss_id] = "epic"
				else:
					rankings["guild"]["execution"]["rank_class"][boss_id] = "rare"
			elif x > 25:
				rankings["guild"]["execution"]["rank_class"][boss_id] = "uncommon"
			else:
				rankings["guild"]["execution"]["rank_class"][boss_id] = "common"
		except:
			rankings["guild"]["execution"]["rank_class"][boss_id] = "common"
		rankings["guild"]["execution"]["deaths"][boss_id] = row.findAll("td")[5].contents[0]
		rankings["guild"]["execution"]["damage_taken"][boss_id] = row.findAll("td")[6].contents[0]
	table = soup.findAll("table")[1]
	for row in table.findAll("tr")[1:]:
		rankings["guild"]["speed"]["rank"][boss_id] = row.findAll("td")[0].contents[0]
		try:
			x = int(rankings["guild"]["speed"]["rank"][boss_id])
			if x > 50:
				if x > 75:
					if x > 95:
						rankings["guild"]["speed"]["rank_class"][boss_id] = "legendary"
					else:
						rankings["guild"]["speed"]["rank_class"][boss_id] = "epic"
				else:
					rankings["guild"]["speed"]["rank_class"][boss_id] = "rare"
			elif x > 25:
				rankings["guild"]["speed"]["rank_class"][boss_id] = "uncommon"
			else:
				rankings["guild"]["speed"]["rank_class"][boss_id] = "common"
		except:
			rankings["guild"]["speed"]["rank_class"][boss_id] = "common"
		rankings["guild"]["speed"]["duration"][boss_id] = row.findAll("td")[5].contents[0]
	return rankings

def analyze(log_id):
	response = get_fights_from_log_id(log_id)
	kills = find_boss_fights(response, log_id)
	details = scrape_rankings(kills)
	report = {"kills": kills, "details": details}
	return report


def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True

def logs_new_guild(guild_name, guild_server, guild_region):
	guild = {}
	guild["guild_name"] = guild_name
	guild["guild_server"] = guild_server
	guild["guild_region"] = guild_region
	guild["logs"] = []
	start_time = 1435734000000
	response = requests.get("https://www.warcraftlogs.com:443/v1/reports/guild/"+guild_name+"/"+guild_server+"/"+guild_region+"?start="+str(start_time)+"&api_key=9457bbf774422ab14b5625efb2b35e36")
	response = json.loads(response.text)
	# print response
	for log in response:
		# print log
		# print log["zone"]
		if log["zone"] == 8:
			new_log = {}
			new_log["log_id"] = log["id"]
			new_log["title"] = log["title"]
			new_log["start"] = log["start"]/1000
			new_log["date"] = datetime.date.fromtimestamp(log["start"]/1000)
			new_log["owner"] = log["owner"]
			guild["logs"].append(new_log)
	guild["last_checked"] = int(time.time())
	guild["last_checked_dt"] = datetime.datetime.fromtimestamp(guild["last_checked"])
	guild_id_string = guild_name+"_"+guild_server+"_"+guild_region
	guild = analyze_guild_logs(guild)
	r.hmset(guild_id_string, guild)
	return guild

def analyze_guild_logs(guild):
	for report in guild["logs"]:
		# print report
		try:
			# "About to check if I have a report"
			analyzed = r.hgetall(report["log_id"])
			if is_empty(analyzed) == True:
				analyzed = analyze(report["log_id"])
				boss_list = analyzed["kills"]
				rankings = analyzed["details"]
				guild_name = rankings["guild_name"]
				r.hmset(report, analyzed)
			# 	print "I analyzed a report"
			# else:
			# 	print "I already had it"
		except:
			report["validity"] = "bad"
			bad_logs = True
			# print "I set a report to bad"
	if bad_logs == True:
		guild["logs"][:] = [d for d in guild["logs"] if d.get('validity') != "bad"]
		# print "I tried to delete bad logs"
	return guild



