# Lucas Schaefer - ljschaef
# Final Project SI 206

import requests
import sqlite3
from bs4 import BeautifulSoup
import plotly
import json

DBNAME = 'final_project.db'
# INFO : Name, Fight Name, Age, Height, Weight, Record, KOs, Subs, Decisions
CACHELISTS = 'final_project.csv'
name_list = []
fightname_list = []
age_list = []
height_list = []
weight_list = []
wins_list = []
losses_list = []
draws_list = []
ncs_list = []
kos_list = []
subs_list = []
decisions_list = []
# Cache of all the html shit, so you don't scape a page you already have
CACHEPAGES = 'final_project.json'
url_and_html_dict = {}

# This is URL for 1st page of all fighters regardless of weight and gender
# From here can crawl to fighter page, grab details, go to next one until done
# with page, then go to next page until all pages have been scraped
baseurl = 'http://www.ufc.com/fighter/Weight_Class'

def create_db():



    pass

def populate_db():




    pass

def scrape_shit():

    fighter_link_list = []
    next_page_links_list = []

    # This is also gonna do the caching I think
    page_html = requests.get(baseurl).text
    page_soup = BeautifulSoup(page_html, 'html.parser')

    # class="fighter-info" then find <a href>

    thing = page_soup.find_all(class_='fighter-info')
    new_thing = page_soup.find(class_='pagination')
    new_thing = new_thing.find('a')['href']

    # thing = thing[0]
    # thing = thing.find('a')['href']
    # print(thing)

    print(new_thing)

    for fighter in thing:
        fighter_link = fighter.find('a')['href']
        fighter_link_list.append(fighter_link)


    for link in fighter_link_list:
        new_url = baseurl + str(link)
        new_html = requests.get(new_url)
        new_soup = BeautifulSoup(new_html, 'html.parser')
        firstname = new_soup.find()
        lastname = new_soup.find()
        name = str(firstname) + ' ' + str(lastname)
        fightname = new_soup.find(id_='fighter-nickname')
        age = new_soup.find()
        height = new_soup.find()
        weight = new_soup.find()
        record = new_soup.find()



    pass

scrape_shit()
