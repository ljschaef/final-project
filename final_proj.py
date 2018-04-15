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

class Fighter():

    def __init__(self, name, fight_name, age, height, weight, record, reach, leg_reach):
        self.name = name
        self.fightname = fight_name
        self.age = age
        self.height = height
        self.weight = weight
        self.record = record
        self.reach = reach
        self.legreach = leg_reach

    def __str__(self):
        statement = str(self.name) + ' is a ' + str(self.weight) + ' pound, ' + \
                    str(self.height) + ' tall fighter known as ' + \
                    str(self.fightname) + '. '
        statement += str(self.fightname) + ' has a reach of ' + str(self.reach) \
                     + ' and a leg reach of ' + str(self.legreach) + \
                     ' and a record of ' + str(self.record) + ' (W-L-D).'

        return statement

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
            'Name' TEXT PRIMARY KEY,
            'FightName' TEXT,
            'Age' INTEGER,
            'Height' TEXT,
            'Weight' TEXT,
            'Record' TEXT,
            'Reach' TEXT,
            'Leg Reach' TEXT
        );
    '''

    cur.execute(statement)

    conn.commit()
    conn.close()

    pass
# create_db()

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

    hacky_url = '/fighter/Weight_Class/filterFighters?offset='
    hacky_part2 = '&max=20&sort=lastName&order=asc&weightClass=&fighterFilter=Current'

    name_list = []
    fightname_list = []
    age_list = []
    height_list = []
    weight_list = []
    record_list = []
    reach_list = []
    legreach_list = []
    fighter_link_list = []
    other_dicc = {}
    dicc = {}
    page_links_list = []

    # This is also gonna do the caching I think
    page_links_list.append(baseurl)

    page_html = requests.get(baseurl).text
    page_soup = BeautifulSoup(page_html, 'html.parser')

    # class="fighter-info" then find <a href>

    # Need to do a thing here that goes to the next page and gets all the
    # fighters there. Does this throughout all the pages. Then I can go ahead
    # and do the rest of the stuff

    thing = page_soup.find_all(class_='fighter-info')
    new_thing = page_soup.find(class_='pagination')
    new_thing = new_thing.find('a')['href']
    page_links_list.append(new_thing)

    damn = truly_baseurl + str(new_thing)
    god_dammit = requests.get(damn).text
    holy_fuck = BeautifulSoup(god_dammit, 'html.parser')
    shit_tits = holy_fuck.find_all(class_='fighter-info')

    for fighter in thing:
        fighter_link = fighter.find('a')['href']
        fighter_link_list.append(str(fighter_link))

    other_dicc[str(baseurl)] = fighter_link_list

    new_list = []
    for fighter in shit_tits:
        fighter_link = fighter.find('a')['href']
        fighter_link_list.append(str(fighter_link))
        new_list.append(str(fighter_link))

    other_dicc[str(damn)] = new_list

    offset = 40

    while offset <= 680:
        newest_list = []
        whole_url = hacky_url + str(offset) + hacky_part2
        truly_whole = truly_baseurl + whole_url
        page_links_list.append(whole_url)
        hacked = requests.get(truly_whole).text
        hacked_soup = BeautifulSoup(hacked, 'html.parser')
        getting_there = hacked_soup.find_all(class_='fighter-info')
        other_dicc[whole_url] = getting_there
        for person in getting_there:
            person_link = person.find('a')['href']
            fighter_link_list.append(person_link)
            newest_list.append(str(person_link))
        other_dicc[str(whole_url)] = newest_list
        offset += 20

    # print("Hit the big for loop")
    # counter = 1
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

        fightname = new_soup.find(id='fighter-nickname')
        if fightname is not None:
            fightname = fightname.text
        else:
            fightname = 'N/A'
        age = new_soup.find(id='fighter-age')
        if age is not None:
            age = age.text
        else:
            age = 'N/A'
        height = new_soup.find(id='fighter-height')
        if height is not None:
            height = height.text
        else:
            height = 'N/A'
        weight = new_soup.find(id='fighter-weight')
        if weight is not None:
            weight = weight.text
        else:
            weight = 'N/A'
        reach = new_soup.find(id='fighter-reach')
        if reach is not None:
            reach = reach.text
        else:
            reach = 'N/A'
        legreach = new_soup.find(id='fighter-leg-reach')
        if legreach is not None:
            legreach = legreach.text
        else:
            legreach = 'N/A'
        record = new_soup.find(id='fighter-skill-record')
        if record is not None:
            record = record.text
        else:
            record = 'N/A'

        fightname_list.append(fightname)
        age_list.append(age)
        height_list.append(height)
        weight_list.append(weight)
        reach_list.append(reach)
        legreach_list.append(legreach)
        record_list.append(record)
        # print(counter)
        # counter += 1
        # '''

    # This is where I will cache 'other_dicc' to a JSON file
    with open(CACHEPAGES, 'w') as f:
        # json.dump(other_dicc, f)
        welp = json.dumps(other_dicc)
        f.write(welp)
        f.close()

    # This is where I will cache all of the lists to a CSV file
    first_line = ['Name', 'Fight Name', 'Age', 'Weight', 'Record', 'Reach',
                  'Leg Reach']
    with open(CACHELISTS, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(first_line)
        # print(first_line)
        # Maybe try to put all of the lists into a dictionary with each person
        # getting their own list Could then try to do write rows each one as an
        # entry in the dict
        # Or make a new list
        # writer.writerows()
        fuck = []
        for i in range(len(name_list)):
            # writer = csv.writer(f)
            frack = [name_list[i], fightname_list[i], age_list[i],
                     weight_list[i], record_list[i], reach_list[i],
                     legreach_list[i]]
            fuck.append(frack)
        writer.writerows(fuck)
        # for row in fuck:
        #     print(row)

    # print(len(fightname_list))
    # print(fightname_list)
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
    dicc['record'] = record_list

    # print("At the end but won't exit for some reason")

    return dicc

scrape_shit()

def utilize_cache():

    # This is gonna check if the csv is filled to 685 rows (header row is included)
    # and if it is will access cache and create instances of fighters
    # If not it will run scrape_shit() and then create the instances once csv is filled

    with open(CACHELISTS) as f:
        thing = csv.reader(f)

    if thing is not None:
        for row in thing:
            name = row[0]


    pass

def make_distribution():

    # this will make distribution graphs

    pass

def make_individual():

    # this will make individual graphs

    pass

def interactive_part():

    # Lets you get info about fighter
    # Maybe make a function that creates and returns a dict of fighters with the
    # index being their name and the other being the instance
    # Function would utilize cache to make instances n shit

    # 3 things here
    # 1: See some distribution graphs (height, reach, weight)
    # 2: Learn about a specific fighter (either input a valid name or get a random one)
    # 3: Then can see visuals for fighter (record, reach vs. leg reach) or go back to initial page

    statement = 'Would you like to see some distribution graphs (input ' \
                '"Distribution"), see info for a specific fighter (input valid ' \
                'name), or see info for a random fighter (input "Rando")?'
    user = input(statement)

    if user == 'Distribution':

        pass

    elif user == 'Rando':

        pass

    else:

        pass
