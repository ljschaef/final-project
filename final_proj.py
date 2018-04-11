# Lucas Schaefer - ljschaef
# Final Project SI 206

import requests
import sqlite3
from bs4 import BeautifulSoup
import plotly
import json

DBNAME = 'final_project.db'
# INFO : Name, Fight Name, Gender, Feet, Inches, Weight, Wins, Losses, Draws,
# NCs, KOs, Subs, Decisions
CACHELISTS = 'final_project.csv'
name_list = []
fightname_list = []
gender_list = []
feet_list = []
inches_list = []
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

    # This is also gonna do the caching I think
    page_html = requests.get(baseurl).text
    page_soup = BeautifulSoup(page_html, 'html.parser')

    

    pass

