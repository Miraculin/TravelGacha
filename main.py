import constants
import gacha
from flask import Flask
from flask import render_template
from flask import url_for

import json

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
    return render_template('roll.html.j2', item=country_result)
        
# if __name__ == "__main__":
#     for k in constants.TIER_PROBABILITY.keys():
#         print(k)