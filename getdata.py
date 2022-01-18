import sqlite3
import json
import urllib.error
import ssl
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('covid19.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS states
    (id_state INTEGER PRIMARY KEY AUTOINCREMENT, 
    code VARCHAR(2) UNIQUE,
    name VARCHAR(50)
    )''')

cur.execute('''CREATE TABLE IF NOT EXISTS covid_stats
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_state_id INTEGER,
    new_cases INTEGER,
    new_death INTEGER,
    creation_date TEXT)
    ''')

cur.execute('''CREATE TABLE IF NOT EXISTS vaccine_stats
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_state_id INTEGER,
    administered INTEGER,
    adm_date TEXT)
    ''')  

#Get Data
#App Token not include. If you wish try with the Token go to https://data.cdc.gov/login
statesurl = "https://gist.githubusercontent.com/mshafrir/2646763/raw/8b0dbb93521f5d6889502305335104218454c2bf/states_hash.json"
covidurl = "https://data.cdc.gov/resource/9mfq-cb36.json"
vaccineurl = "https://data.cdc.gov/resource/rh2h-3yt2.json"

print('Retrieving...')
uh_state = urllib.request.urlopen(statesurl, context=ctx)
data_state = uh_state.read().decode()
uh_covid = urllib.request.urlopen(covidurl, context=ctx)
data_covid = uh_covid.read().decode()
uh_vaccine = urllib.request.urlopen(vaccineurl, context=ctx)
data_vaccine = uh_vaccine.read().decode()

try:
    jsState = json.loads(data_state)
except:
    print(data_state)  # We print in case unicode causes an error
    pass

try:
    jsCovid = json.loads(data_covid)
except:
    print(data_covid)  # We print in case unicode causes an error
    pass

try:
    jsVaccine = json.loads(data_vaccine)
except:
    print(data_vaccine)  # We print in case unicode causes an error
    pass

retrieved = len(data_state) + len(data_covid) + len(data_vaccine)

print('Retrieved:', retrieved, 'characters')

#Save Data

cur.execute('SELECT COUNT(*) FROM states')
numStates = cur.fetchone()[0]
for element in jsState:
    cur.execute('''INSERT OR IGNORE INTO states (code, name) 
        VALUES ( ?, ? )''', ( element, jsState[element] ) )
    conn.commit()
cur.execute('SELECT COUNT(*) FROM states')
addStates = cur.fetchone()[0]

print('Table states:', 'Existing records =', numStates, 'Records added:', int(addStates) - int(numStates))

cur.execute('SELECT COUNT(*) FROM covid_stats')
numCovid = cur.fetchone()[0]
for element in jsCovid:
    state = element['state']
    newCases = element['new_case']
    newDeaths = element['new_death']
    date = element['created_at']
    cur.execute('SELECT id_state FROM states WHERE code = ?', ( state, ))
    try:
        id_state = cur.fetchone()[0]
        cur.execute('''SELECT * FROM covid_stats
            WHERE fk_state_id = ?
            AND new_cases = ?
            AND new_death = ?
            AND creation_date = ?''', (id_state,newCases,newDeaths,date))
        row = cur.fetchone()
        if row is None:
            cur.execute('''INSERT INTO covid_stats (fk_state_id, new_cases, new_death, creation_date) 
            VALUES ( ?, ?, ?, ? )''', ( id_state, newCases, newDeaths, date ) )
        conn.commit()
    except:
        continue
cur.execute('SELECT COUNT(*) FROM covid_stats')
addCovid = cur.fetchone()[0]

print('Table covid_stats:', 'Existing records =', numCovid, 'Records added:', int(addCovid) - int(numCovid))

cur.execute('SELECT COUNT(*) FROM vaccine_stats')
numVaccine = cur.fetchone()[0]
for element in jsVaccine:
    if(element['date_type'] == 'Admin'):
        state = element['location']
        admin = element['administered_daily']
        date = element['date']
        cur.execute('SELECT id_state FROM states WHERE code = ?', ( state, ))
        try:
            id_state = cur.fetchone()[0]
            cur.execute('''SELECT * FROM vaccine_stats
                WHERE fk_state_id = ?
                AND administered = ?
                AND adm_date = ?''', (id_state,admin,date))
            row = cur.fetchone()
            if row is None:
                cur.execute('''INSERT INTO vaccine_stats (fk_state_id, administered, adm_date) 
                VALUES ( ?, ?, ? )''', ( id_state, admin,  date ) )
            conn.commit()
        except:
            continue
cur.execute('SELECT COUNT(*) FROM vaccine_stats')
addVaccine = cur.fetchone()[0]

print('Table covid_stats:', 'Existing records =', numVaccine, 'Records added:', int(addVaccine) - int(numVaccine))
