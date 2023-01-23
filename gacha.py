import constants
import random
import hashlib
import requests
from bs4 import BeautifulSoup
import json

def roll_gacha():
    ran_result = random.uniform(0,1)
    tier_result = ""
    result = ""
    for k,v in constants.TIER_PROBABILITY.items():
        if ran_result >= v:
            tier_result = k
            break
    #print(ran_result)
    #print(len(constants.COUNTRY_TIER[tier_result]))
    ran_country = constants.COUNTRY_TIER[tier_result][random.randint(0, len(constants.COUNTRY_TIER[tier_result])-1)]
    return generateResult(tier_result, ran_country)

def generateResult(tier, country):
    underscore_country = country.replace(" ", "_").replace("&", "and").split(" (")[0]
    #print(ran_country)
    md5sum1 = hashlib.md5(f"{underscore_country}_Banner.jpg".encode('utf-8')).hexdigest()
    md5sum2 = hashlib.md5(f"{underscore_country}_banner.jpg".encode('utf-8')).hexdigest()

    href1 = f"https://wikitravel.org/upload/shared/{md5sum1[0]}/{md5sum1[:2]}/{underscore_country}_Banner.jpg"
    href2 = f"https://wikitravel.org/upload/shared/{md5sum2[0]}/{md5sum2[:2]}/{underscore_country}_banner.jpg"

    href1_response = requests.get(href1)
    href = ""
    print(href1_response.status_code)

    if href1_response.status_code != 404:
        href = href1
    else: 
        href2_response = requests.get(href2)
        print(href2_response.status_code)
    
        if href2_response.status_code != 404:
            href = href2

    response = requests.get(f'https://wikitravel.org/en/{underscore_country}')

    soup = BeautifulSoup(response.content, 'html.parser')
    #print(soup)
    blurb_div = soup.find_all("div", class_="mw-parser-output")[0]
    blurbs = blurb_div.find_all("p", recursive = False)
    blurb = None
    for b in blurbs:
        print(b.get_text(), len(b.get_text()))
        if len(b.get_text()) > 1:
            blurb = b.get_text()
            break

    wikiVoyage_link = f'https://wikivoyage.org/wiki/{underscore_country}'

    #     response = requests.get('https://wikitravel.org/wiki/en/api.php?action=query&format=json&prop=revisions&titles={underscore_country}&formatversion=2&rvprop=content')
    # wiki_response = json.loads(response.content)
    # print(wiki_response)
    country_result = {
        "country": country,
        "href": href,
        "tier": tier,
        "blurb": blurb,
        "wikiVoyage": wikiVoyage_link
    }

    return country_result

def find_country(country_name):
    for k,v in constants.COUNTRY_TIER.items():
        for j in v:
            if j == country_name:
                return generateResult(k,j)
    return None