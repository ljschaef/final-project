# Lucas Schaefer - ljschaef
# Final Project SI 206

import requests
import sqlite3
from bs4 import BeautifulSoup
import plotly
import json
import csv

DBNAME = 'final_project.db'
# INFO : Name, Fight Name, Age, Height, Weight, Record, Reach, Leg Reach
CACHELISTS = 'final_project.csv'

# Cache of all the html shit, so you don't scape a page you already have
CACHEPAGES = 'final_project.json'
url_and_html_dict = {}

# This is URL for 1st page of all fighters regardless of weight and gender
# From here can crawl to fighter page, grab details, go to next one until done
# with page, then go to next page until all pages have been scraped
baseurl = 'http://www.ufc.com/fighter/Weight_Class'
truly_baseurl = 'http://www.ufc.com'

def create_db():

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = '''
        DROP TABLE IF EXISTS 'Fighters';
    '''

    cur.execute(statement)

    conn.commit()

    statement = '''
        CREATE TABLE 'Fighters'(
            'Name' TEXT PRIMARY KEY
            'Fight Name' TEXT
            'Age' INTEGER 
            'Height' TEXT
            'Weight' TEXT
            'Record' TEXT
            'Reach' TEXT
            'Leg Reach' TEXT
        );
    '''

    cur.execute(statement)

    conn.commit()
    conn.close()

    pass

def populate_db():

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    with open(CACHELISTS) as cache:
        fighter_info = csv.reader(cache)
        row_num = 0
        for row in fighter_info:
            if row_num == 0:
                row_num += 1
            else:
                insertion = (row[0], row[1], row[2], row[3], row[4], row[5],
                             row[6], row[7])
                statement = 'INSERT INTO "Fighters" '
                statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
                cur.execute(statement, insertion)


    pass

def scrape_shit():

    name_list = []
    fightname_list = []
    age_list = []
    height_list = []
    weight_list = []
    record_list = []
    reach_list = []
    legreach_list = []
    fighter_link_list = []
    dicc = {}
    next_page_links_list = []

    # This is also gonna do the caching I think
    page_html = requests.get(baseurl).text
    page_soup = BeautifulSoup(page_html, 'html.parser')

    # class="fighter-info" then find <a href>

    # Need to do a thing here that goes to the next page and gets all the
    # fighters there. Does this throughout all the pages. Then I can go ahead
    # and do the rest of the stuff

    thing = page_soup.find_all(class_='fighter-info')
    new_thing = page_soup.find(class_='pagination')
    new_thing = new_thing.find('a')['href']
    next_page_links_list.append(new_thing)
    counter = 2

    # NEED TO CHANGE THE OFFSET NUMBER IN THE URL EACH TIME
    # AUTOINCREMENT BY 20 UNTIL IT HITS LIKE 680 OR WHATEVER THE FINAL ONE IS
    # I'M A FUCKING HACKER LOLOLOLOL

    while counter < 36:
        newy_url = truly_baseurl + str(new_thing)
        bleck = requests.get(newy_url).text
        more_bleh = BeautifulSoup(bleck, 'html.parser')
        shit = more_bleh.find(class_='pagination')
        tits = shit.find_all('li')
        newish_thing = tits[counter]
        new_thing = newish_thing.find('a')['href']
        next_page_links_list.append(new_thing)
        counter += 1
    print(len(next_page_links_list))
    lit = '''
    newy_url = truly_baseurl + str(new_thing)
    bleck = requests.get(newy_url).text
    more_bleh = BeautifulSoup(bleck, 'html.parser')
    shit = more_bleh.find(class_='pagination')
    frack = shit
    frack = frack.find_all('li')
    for row in frack:
        print(row)
    '''
    # SERIOUSLY, LOOK AT THE ABOVE COMMENT LOL

    # thing = thing[0]
    # thing = thing.find('a')['href']
    # print(thing)
    # print(new_thing)

    for fighter in thing:
        fighter_link = fighter.find('a')['href']
        fighter_link_list.append(fighter_link)

    for link in fighter_link_list:
        new_url = truly_baseurl + str(link)
        # print(new_url)
        # fuck = '''
        new_html = requests.get(new_url).text
        new_soup = BeautifulSoup(new_html, 'html.parser')
        possibly_name = new_soup.find(class_='floatl current')
        if possibly_name is not None:
            name = possibly_name.text
            name_list.append(name)
            # print(name)
        else:
            possibly_name = new_soup.find(class_='floatl current contender-series')
            name = possibly_name.text
            name_list.append(name)
            # print(name)

        fightname = new_soup.find(id_='fighter-nickname')
        age = new_soup.find(id_='fighter-age')
        height = new_soup.find(id_='fighter-height')
        weight = new_soup.find(id_='fighter-weight')
        reach = new_soup.find(id_='fighter-reach')
        legreach = new_soup.find(id_='fighter-leg-reach')
        record = new_soup.find(id_='fighter-skill-record')
        fightname_list.append(fightname)
        age_list.append(age)
        height_list.append(height)
        weight_list.append(weight)
        reach_list.append(reach)
        legreach_list.append(legreach)
        record_list.append(record)
        # '''
    # print(len(name_list))
    # print(len(fightname_list))
    # print(len(age_list))
    # print(len(height_list))
    # print(len(weight_list))
    # print(len(reach_list))
    # print(len(legreach_list))
    # print(len(record_list))

    dicc['names'] = name_list
    dicc['fightnames'] = fightname_list
    dicc['ages'] = age_list
    dicc['heights'] = height_list
    dicc['weights'] = weight_list
    dicc['reaches'] = reach_list
    dicc['legreaches'] = legreach_list
    dicc['recors'] = record_list

    return dicc

scrape_shit()
