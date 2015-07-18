from flask import Flask, render_template, redirect, request, url_for, flash, session
import requests
import json
import model
import os
import redis
import ast

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


@app.route("/about")
def about():
	return render_template("about.html")



if __name__ == "__main__":
	app.run(debug = True)