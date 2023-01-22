import constants
import random
from flask import Flask
from flask import render_template
from flask import url_for
import hashlib
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route("/")
def main():
    url_for('static', filename='main.css')
    return render_template('main.html.j2')

@app.route("/roll")
def roll():
    ran_result = random.uniform(0,1)
    tier_result = ""
    result = ""
    for k,v in constants.TIER_PROBABILITY.items():
        if ran_result >= v:
            tier_result = k
            break
    print(ran_result)
    print(len(constants.COUNTRY_TIER[tier_result]))
    ran_country = constants.COUNTRY_TIER[tier_result][random.randint(0, len(constants.COUNTRY_TIER[tier_result])-1)]
    # ran_country = constants.COUNTRY_TIER["S"][1]
    # tier_result = "S"
    underscore_country = ran_country.replace(" ", "_").replace("&", "and").split(" (")[0]
    print(ran_country)
    md5sum1 = hashlib.md5(f"{underscore_country}_Banner.jpg".encode('utf-8')).hexdigest()
    md5sum2 = hashlib.md5(f"{underscore_country}_banner.jpg".encode('utf-8')).hexdigest()

    response = requests.get(f'https://wikitravel.org/en/{underscore_country}')

    soup = BeautifulSoup(response.content, 'html.parser')
    #print(soup)
    blurb = soup.find_all("div", class_="mw-parser-output")[0]
    blurb = blurb.find_all("p", recursive = False)[0]

    wikiVoyage_link = f'https://wikivoyage.org/wiki/{underscore_country}'

    #     response = requests.get('https://wikitravel.org/wiki/en/api.php?action=query&format=json&prop=revisions&titles={underscore_country}&formatversion=2&rvprop=content')
    # wiki_response = json.loads(response.content)
    # print(wiki_response)
    country_result = {
        "country": ran_country,
        "href": f"https://wikitravel.org/upload/shared/{md5sum1[0]}/{md5sum1[:2]}/{underscore_country}_Banner.jpg",
        "href2": f"https://wikitravel.org/upload/shared/{md5sum2[0]}/{md5sum2[:2]}/{underscore_country}_banner.jpg",
        "tier": tier_result,
        "blurb": blurb,
        "wikiVoyage": wikiVoyage_link
    }
    url_for('static', filename='main.css')
    return render_template('roll.html.j2', item=country_result)

        
# if __name__ == "__main__":
#     for k in constants.TIER_PROBABILITY.keys():
#         print(k)