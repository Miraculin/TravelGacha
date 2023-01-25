import constants
import random
import hashlib
import requests
from bs4 import BeautifulSoup
import json
import os


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

def get_banner(country):
    custom_banner_path = os.path.join("custom", f"{country}_banner.jpg")
    cache_banner_path = os.path.join("cache", f"{country}_banner.jpg")
    if os.path.exists(custom_banner_path):
        return custom_banner_path
    elif os.path.exists(cache_banner_path):
        return cache_banner_path
    else:
        md5sum1 = hashlib.md5(f"{country}_Banner.jpg".encode('utf-8')).hexdigest()
        md5sum2 = hashlib.md5(f"{country}_banner.jpg".encode('utf-8')).hexdigest()

        href1 = f"https://wikitravel.org/upload/shared/{md5sum1[0]}/{md5sum1[:2]}/{country}_Banner.jpg"
        href2 = f"https://wikitravel.org/upload/shared/{md5sum2[0]}/{md5sum2[:2]}/{country}_banner.jpg"

        href1_response = requests.get(href1)
        href = ""
        img_response = href1_response.content
        print(href1_response.status_code)

        if href1_response.status_code != 404:
            href = href1
        else: 
            href2_response = requests.get(href2)
            print(href2_response.status_code)
        
            if href2_response.status_code != 404:
                href = href2
                img_response = href2_response.content
        if href != "":
            with open(cache_banner_path, "wb+") as f:
                f.write(img_response)
        return href

def get_blurb(country):
    blurb_cache = os.path.join("cache", f"{country}_blurb.txt")
    if os.path.exists(blurb_cache):
        with open(blurb_cache, "r") as g:
            return g.read()
    else:
        response = requests.get(f'https://wikitravel.org/en/{country}')

        soup = BeautifulSoup(response.content, 'html.parser')
        #print(soup)
        blurb_div = soup.find_all("div", class_="mw-parser-output")[0]
        blurbs = blurb_div.find_all("p", recursive = False)
        blurb = ""
        for b in blurbs:
            print(b.get_text(), len(b.get_text()))
            if len(b.get_text()) > 1:
                blurb = b.get_text()
                break
        with open(blurb_cache, "w+") as g:
            g.write(blurb)
        return blurb

def generateResult(tier, country):
    if not os.path.exists("cache"):
        os.mkdir("cache")
    underscore_country = country.replace(" ", "_").replace("&", "and").split(" (")[0]
    #print(ran_country)
    banner_path = get_banner(underscore_country)
    blurb = get_blurb(underscore_country)

    wikiVoyage_link = f'https://wikivoyage.org/wiki/{underscore_country}'

    #     response = requests.get('https://wikitravel.org/wiki/en/api.php?action=query&format=json&prop=revisions&titles={underscore_country}&formatversion=2&rvprop=content')
    # wiki_response = json.loads(response.content)
    # print(wiki_response)
    country_result = {
        "country": country,
        "href": banner_path,
        "tier": tier,
        "blurb": blurb,
        "wikiVoyage": wikiVoyage_link,
        "tierClass": f'tier{tier if tier != "H" else "B"}',
    }
    print(country_result)
    return country_result

def find_country(country_name):
    for k,v in constants.COUNTRY_TIER.items():
        for j in v:
            if j == country_name:
                return generateResult(k,j)
    return None