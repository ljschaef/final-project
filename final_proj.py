# Lucas Schaefer - ljschaef
# Final Project SI 206

import requests
import sqlite3
from bs4 import BeautifulSoup
import plotly.plotly as py
import plotly.graph_objs as go
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

    def __init__(self, name=None, fight_name=None, age=None, height=None,
                 weight=None, record=None, reach=None, leg_reach=None):
        self.name = name
        self.fightname = fight_name
        self.age = age
        self.height = height
        self.weight = weight
        self.record = record
        self.reach = reach
        self.legreach = leg_reach

    def __str__(self):
        if self.fightname != 'N/A':
            statement = str(self.name) + ' is a ' + str(self.weight) + ' pound, ' + \
                    str(self.height) + ' tall fighter known as ' + \
                    str(self.fightname) + '. '
            statement += str(self.fightname) + ' has a reach of ' + str(self.reach) \
                     + ' inches and a leg reach of ' + str(self.legreach) + \
                     ' inches and a record of ' + str(self.record) + ' (W-L-D).'
        else:
            statement = str(self.name) + ' is a ' + str(self.weight) + ' pound, ' + \
                        str(self.height) + ' tall fighter. '
            statement += str(self.name) + ' has a reach of ' + str(self.reach) \
                         + ' inches, a leg reach of ' + str(self.legreach) + \
                         ' inches, and a record of ' + str(self.record) + ' (W-L-D).'

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
            'Name' TEXT,
            'FightName' TEXT,
            'Age' INTEGER,
            'Height' TEXT,
            'Weight' INTEGER,
            'Record' TEXT,
            'Reach' INTEGER,
            'Leg Reach' INTEGER
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

    conn.commit()
    conn.close()

    pass

# populate_db()

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

    page_links_list.append(baseurl)

    page_html = requests.get(baseurl).text
    page_soup = BeautifulSoup(page_html, 'html.parser')

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

    for link in fighter_link_list:

        new_url = truly_baseurl + str(link)
        # print(new_url)
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
            length = len(height)
            length -= 11
            height = height[0:length]
        else:
            height = 'N/A'
        weight = new_soup.find(id='fighter-weight')
        if weight is not None:
            weight = weight.text
            length = len(weight)
            length -= 13
            weight = weight[0:length]
        else:
            weight = 'N/A'
        reach = new_soup.find(id='fighter-reach')
        if reach is not None:
            reach = reach.text
            length = len(reach)
            length -= 1
            reach = reach[0:length]
        else:
            reach = 'N/A'
        legreach = new_soup.find(id='fighter-leg-reach')
        if legreach is not None:
            legreach = legreach.text
            length = len(legreach)
            length -= 1
            legreach = legreach[0:length]
        else:
            legreach = 'N/A'
        record = new_soup.find(class_='fighter-record')
        if record is not None:
            record = record.text
            length = len(record)
            length -= 9
            record = record[0:length]

        else:
            record = 'N/A'

        fightname_list.append(fightname)
        age_list.append(age)
        height_list.append(height)
        weight_list.append(weight)
        reach_list.append(reach)
        legreach_list.append(legreach)
        record_list.append(record)

    with open(CACHEPAGES, 'w') as f:
        welp = json.dumps(other_dicc)
        f.write(welp)
        f.close()

    first_line = ['Name', 'Fight Name', 'Age', 'Height', 'Weight', 'Record', 'Reach',
                  'Leg Reach']
    with open(CACHELISTS, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(first_line)
        fuck = []
        for i in range(len(name_list)):
            frack = [name_list[i], fightname_list[i], age_list[i],
                     height_list[i], weight_list[i], record_list[i], reach_list[i],
                     legreach_list[i]]
            fuck.append(frack)
        writer.writerows(fuck)

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

    return dicc

# scrape_shit()

def utilize_db():

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = '''
        SELECT *
        FROM Fighters
    '''

    cur.execute(statement)

    name_list = []
    fightname_list = []
    age_list = []
    height_list = []
    weight_list = []
    record_list = []
    reach_list = []
    legreach_list = []

    for row in cur:
        name_list.append(row[0])
        fightname_list.append(row[1])
        age_list.append(row[2])
        height_list.append(row[3])
        weight_list.append(row[4])
        record_list.append(row[5])
        reach_list.append(row[6])
        legreach_list.append(row[7])

    fighter_dict = {}

    for i in range(len(name_list)):
        fighter = Fighter()
        fighter.name = name_list[i]
        fighter.fightname = fightname_list[i]
        fighter.age = age_list[i]
        fighter.height = height_list[i]
        fighter.weight = weight_list[i]
        fighter.record = record_list[i]
        fighter.reach = reach_list[i]
        fighter.legreach = legreach_list[i]
        fighter_dict[fighter.name] = fighter

    # print(len(fighter_dict))
    # print(fighter_dict['Jose Aldo'])

    return fighter_dict

# utilize_db()

def make_distribution(dicc, command):

    age_list = []
    weight_list = []
    reach_list = []

    for a in dicc:
        b = dicc[a]
        # print(b)
        age = b.age
        weight = b.weight
        reach = b.reach
        age_list.append(age)
        weight_list.append(weight)
        reach_list.append(reach)

    # print(len(age_list))
    # print(len(weight_list))
    # print(len(reach_list))

    age1 = 0
    age2 = 0
    age3 = 0
    age4 = 0
    age5 = 0
    age6 = 0
    for i in range(len(age_list)):
        da_age = age_list[i]
        if da_age != 'N/A':
            da_age = int(da_age)
            if 20 <= da_age <= 25:
                age1 += 1
            elif 26 <= da_age <= 30:
                age2 += 1
            elif 31 <= da_age <= 35:
                age3 += 1
            elif 36 <= da_age <= 40:
                age4 += 1
            else:
                age5 += 1
        else:
            age6 += 1

    weight1 = 0
    weight2 = 0
    weight3 = 0
    weight4 = 0
    weight5 = 0
    weight6 = 0
    weight7 = 0
    weight8 = 0
    weight9 = 0
    weight10 = 0

    for i in range(len(weight_list)):
        da_weight = weight_list[i]
        if da_weight != 'N/A':
            if da_weight == 115:
                weight1 += 1
            elif da_weight == 125:
                weight2 += 1
            elif da_weight == 135:
                weight3 += 1
            elif da_weight == 145:
                weight4 += 1
            elif da_weight == 155:
                weight5 += 1
            elif da_weight == 170:
                weight6 += 1
            elif da_weight == 185:
                weight7 += 1
            elif da_weight == 205:
                weight8 += 1
            else:
                weight9 += 1
        else:
            weight10 += 1

    reach1 = 0
    reach2 = 0
    reach3 = 0
    reach4 = 0
    reach5 = 0
    reach6 = 0

    for i in range(len(reach_list)):
        da_reach = reach_list[i]
        if da_reach != 'N/A':
            if 60 <= da_reach <= 65:
                reach1 += 1
            elif 66 <= da_reach <= 70:
                reach2 += 1
            elif 71 <= da_reach <= 75:
                reach3 += 1
            elif 76 <= da_reach <= 80:
                reach4 += 1
            else:
                reach5 += 1
        else:
            reach6 += 1

    if command == 'age':
        age_data = [go.Bar(
                    x=['20-25', '26-30', '31-35', '36-40', '41-44', 'N/A'],
                    y=[age1, age2, age3, age4, age5, age6]
        )]
        layout = go.Layout(title='Distribution of Fighters Age')
        fig = go.Figure(data=age_data, layout=layout)
        py.plot(fig, filename='Age-Range-of-Fighters')

    elif command == 'weight':
        weight_data = [go.Bar(
                        x=['115', '125', '135', '145', '155', '170', '185', '205',
                           '206-265', 'N/A'],
                        y=[weight1, weight2, weight3, weight4, weight5, weight6,
                           weight7, weight8, weight9, weight10]
        )]
        layout = go.Layout(title='Distribution of Fighters Weight')
        fig = go.Figure(data=weight_data, layout=layout)
        py.plot(fig, filename='Weight-Range-of-Fighters')

    elif command == 'reach':
        reach_data = [go.Bar(
                        x=['60-65', '66-70', '71-75', '76-80', '81-84', 'N/A'],
                        y=[reach1, reach2, reach3, reach4, reach5, reach6]
        )]
        layout = go.Layout(title='Distribution of Fighters Reach')
        fig = go.Figure(data=reach_data, layout=layout)
        py.plot(fig, filename='Reach-Range-of-Fighters')
    else:
        print('That was not a valid command.')

    pass

# dicc = utilize_db()
# make_distribution(dicc, 'reach')

def make_individual(dicc, name):

    # this will make individual graphs
    fighter = dicc.get(name)
    if fighter is None:
        you_messed_up = 'C\'mon, you were told to input a valid name'
        return you_messed_up
    record = fighter.record

    wins = 0
    losses = 0
    draws = 0
    tits = 0
    if record[1] == '-':
        wins = int(record[0])
        if record[3] == '-':
            losses = int(record[2])
            draws = int(record[4])
        else:
            losses = int(record[2:4])
            draws = int(record[5])
    elif record[2] == '-':
        wins = record[0:2]
        if record[4] == '-':
            losses = int(record[3])
            draws = int(record[5])
        else:
            losses = int(record[3:5])
            draws = int(record[6])
    else:
        tits = 1

    if tits == 0:
        # This is where we make the plotly graph

        labels = ['Wins', 'Losses', 'Draws']
        values = [wins, losses, draws]
        trace = go.Pie(labels=labels, values=values, hoverinfo='label+percent', textinfo='value')
        fuck = 'Record of Fighter You Input'
        layout = go.Layout(title=fuck)
        fig = go.Figure(data=[trace], layout=layout)
        py.plot(fig, filename='Record')

    else:
        statement = 'No graph can be made because this fighter\'s record isn\'t ' \
                    'available'
        print(statement)

    gucci = 'Well, that\'s your graph'

    return gucci

# dicc = utilize_db()
# make_individual(dicc, 'Jose Aldo')

def interactive_part():

    statement = 'Would you like to see some distribution graphs (input ' \
                '"Distribution"),\n see info for a specific fighter (input valid ' \
                'name)\n or leave the program (input "Exit")?'
    user = input(statement)

    dicc = utilize_db()

    if dicc == {}:
        no_cache = 'Hold up, need to scrape stuff. Buckle up for this long ride.'
        print(no_cache)
        dicc = scrape_shit()
        populate_db()
    else:
        theres_cache = 'You\'re in luck. The cache has already been filled'
        print(theres_cache)

    while user != 'Exit':
        if user == 'Distribution':
            new_statement = 'Input "age" if you want to see distribution of age among fighters.\n '
            new_statement += 'Input "weight" if you want to see distribution of weight among fighters.\n '
            new_statement += 'Input "reach" if you want to see distribution of  among fighters.'
            stuff = input(new_statement)
            make_distribution(dicc, stuff)

        elif user == 'Exit':
            print('Thanks for using me!')
            break

        else:
            thing = make_individual(dicc, user)
            print(thing)

        statement = 'Would you like to see some distribution graphs (input ' \
                    '"Distribution"),\n see info for a specific fighter (input valid ' \
                    'name)\n or leave the program (input "Exit")?'
        user = input(statement)
    print('Thanks for using me!')

    pass
if __name__ == '__main__':
    interactive_part()

# NEED TO MAKE TESTS FUCK ME
