from flask import Flask, render_template, redirect, request, url_for, flash, session
import requests
import json
import model
import os

app = Flask(__name__)
try:
	app.secret_key = os.environ['FLASK_KEY']
except:
	import config
	app.secret_key = config.FLASK_KEY

@app.route("/")
def index():
	return render_template("index.html")


@app.route("/report")
def report():
	report = request.args.get("report")
	report = report[-16:]
	analyzed = model.analyze(report)
	boss_list = analyzed[0]
	players = analyzed[1]
	simple_boss_list = ["Hellfire Assault", "Iron Reaver"]
	return render_template("report.html", boss_list=boss_list, players=players, simple=simple_boss_list)




if __name__ == "__main__":
	app.run(debug = True)