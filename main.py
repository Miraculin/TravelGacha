import constants
import gacha
from flask import Flask
from flask import render_template
from flask import url_for
import os
from flask import send_from_directory

app = Flask(__name__)

@app.route("/")
def main():
    url_for('static', filename='main.css')
    return render_template('main.html.j2')

@app.route("/roll")
def roll():
    country_result = gacha.roll_gacha()
    url_for('static', filename='main.css')
    return render_template('roll.html.j2', item=country_result)

@app.route("/debug/<country>")
def debug(country):
    country_result = gacha.find_country(country)
    if country_result != None:
        if country_result['href'].startswith("custom") or country_result['href'].startswith("cache"):
            country_result['href'] = url_for(country_result['href'].split(os.sep)[0], filename=country_result['href'].split(os.sep)[1])
    return render_template('roll.html.j2', item=country_result)
        
@app.route('/cache/<path:filename>')
def cache(filename):
    return send_from_directory(app.root_path + '/cache/', filename)

@app.route('/custom/<path:filename>')
def custom(filename):
    return send_from_directory(app.root_path + '/custom/', filename)
