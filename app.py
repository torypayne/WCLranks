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





if __name__ == "__main__":
	app.run(debug = True)