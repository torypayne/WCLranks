from flask import Flask, render_template, redirect, request, url_for, flash, session
import requests
import json
import model
import os
import redis
import ast
import datetime

app = Flask(__name__)
try:
	app.secret_key = os.environ['FLASK_KEY']
	r = redis.from_url(os.environ.get('REDIS_URL'))
except:
	import config
	app.secret_key = config.FLASK_KEY
	r = redis.from_url(config.REDIS_URL)
	


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/report")
def report():
	report = request.args.get("report")
	report = report[-16:]
	try:
		try:
			analyzed = r.hgetall(report)
			boss_list = analyzed["kills"]
			rankings = analyzed["details"]
			boss_list = ast.literal_eval(boss_list)
			rankings = ast.literal_eval(rankings)
			return render_template("report.html", boss_list=boss_list, rankings=rankings, report=report)
		except:
			analyzed = model.analyze(report)
			boss_list = analyzed["kills"]
			rankings = analyzed["details"]
			r.hmset(report, analyzed)
			return render_template("report.html", boss_list=boss_list, rankings=rankings, report=report)
	except:
		return render_template("badlog.html")

@app.route("/report", methods=["POST"])
def refresh_report():
	try:
		report = request.args.get("report")
		report = report[-16:]
		r.delete(report)
		analyzed = model.analyze(report)
		boss_list = analyzed["kills"]
		rankings = analyzed["details"]
		r.hmset(report, analyzed)
		return render_template("report.html", boss_list=boss_list, rankings=rankings, report=report)
	except:
		return render_template("badlog.html")


@app.route("/guildcalendar")
def guild_calendar():
	return render_template("guild_calendar.html")

@app.route("/guild_reports/<guild_name>/<guild_server>/<guild_region>")
def guild_reports(guild_name, guild_server, guild_region):
	# guild_name = request.args.get("guild_name")
	# guild_server = request.args.get("guild_server")
	# guild_region = request.args.get("guild_region")
	guild = model.logs_new_guild(guild_name, guild_server, guild_region)
	guild = model.analyze_guild_logs(guild)
	return render_template("guild_list.html", guild=guild)

@app.route("/guild_list")
def guild_list():
	guild_name = request.args.get("guild").title()
	guild_server = request.args.get("server").title()
	guild_region = request.args.get("region").upper()
	guild_id_string = guild_name+"_"+guild_server+"_"+guild_region
	redis_guild = r.hgetall(guild_id_string)
	if model.is_empty(redis_guild) == True:
		guild = model.logs_new_guild(guild_name, guild_server, guild_region)
	else:
		# print redis_guild
		guild = {}
		guild["guild_name"] = redis_guild["guild_name"]
		guild["guild_server"] = redis_guild["guild_server"]
		guild["guild_region"] = redis_guild["guild_region"]
		guild["logs"] = eval(redis_guild["logs"])
	return render_template("guild_list.html", guild=guild)

@app.route("/guild_list", methods=["POST"])
def update_guild_list():
	guild_name = request.args.get("guild").title()
	guild_server = request.args.get("server").title()
	guild_region = request.args.get("region").upper()
	guild = model.refresh_guild_logs(guild_name, guild_server, guild_region, r)
	return render_template("guild_list.html", guild=guild)

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/badlog")
def badlog():
	return render_template("badlog.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
	app.run(debug = True)