import sqlite3

conn = sqlite3.connect('covid19.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS cases
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    fk_state_id INTEGER,
    month TEXT,
    cases INTEGER
    )''')

cur.execute('''CREATE TABLE IF NOT EXISTS deaths
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    fk_state_id INTEGER,
    month TEXT,
    deaths INTEGER
    )''')

cur.execute('''CREATE TABLE IF NOT EXISTS vaccines
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    fk_state_id INTEGER,
    month TEXT,
    vaccines INTEGER
    )''')


cur.execute('SELECT * FROM states')

states = list()
for element in cur:
    states.append(element[0])

cases = dict()
deaths = dict()
vaccines = dict()
insertsC = 0
updatesC = 0
insertsD = 0
updatesD = 0
insertsV = 0
updatesV = 0
for state in states:
    cur.execute('SELECT * FROM covid_stats WHERE fk_state_id = ? ORDER BY creation_date', (state, ))
    for element in cur:
        month = element[4][:7]
        cases[month] = cases.get(month,0) + element[2]
        deaths[month] = deaths.get(month,0) + element[3]
    for case in cases:
        id_state = state
        count = cases[case]
        cur.execute('SELECT COUNT(*) FROM cases WHERE fk_state_id = ? AND month = ?', ( id_state, case ))
        row = cur.fetchone()
        if row[0] == 0:
            cur.execute('INSERT INTO cases (fk_state_id,month,cases) VALUES (?,?,?)', ( id_state, case, count ))
            insertsC = insertsC + 1
        else:
            cur.execute('UPDATE cases SET cases = ? WHERE fk_state_id = ? AND month = ?', ( count, id_state, case ))
            updatesC = updatesC + 1
    conn.commit()
    for death in deaths:
        id_state = state
        count = deaths[death]
        cur.execute('SELECT COUNT(*) FROM deaths WHERE fk_state_id = ? AND month = ?', ( id_state, death ))
        row = cur.fetchone()
        if row[0] == 0:
            cur.execute('INSERT INTO deaths (fk_state_id,month,deaths) VALUES (?,?,?)', ( id_state, death, count ))
            insertsD = insertsD + 1
        else:
            cur.execute('UPDATE deaths SET deaths = ? WHERE fk_state_id = ? AND month = ?', ( count, id_state, death ))
            updatesD = updatesD + 1
    conn.commit()
    cur.execute('SELECT * FROM vaccine_stats WHERE fk_state_id = ? ORDER BY adm_date', (state, ))
    for element in cur:
        month = element[3][:7]
        vaccines[month] = vaccines.get(month,0) + element[2]
    for admin in vaccines:
        id_state = state
        count = vaccines[admin]
        cur.execute('SELECT COUNT(*) FROM vaccines WHERE fk_state_id = ? AND month = ?', ( id_state, admin ))
        row = cur.fetchone()
        if row[0] == 0:
            cur.execute('INSERT INTO vaccines (fk_state_id,month,vaccines) VALUES (?,?,?)', ( id_state, admin, count ))
            insertsV = insertsV + 1
        else:
            cur.execute('UPDATE vaccines SET vaccines = ? WHERE fk_state_id = ? AND month = ?', ( count, id_state, admin ))
            updatesV = updatesV + 1
    conn.commit()
print('Table cases: Inserts->',insertsC,'Updates->',updatesC)
print('Table deaths: Inserts->',insertsD,'Updates->',updatesD)
print('Table vaccines: Inserts->',insertsV,'Updates->',updatesV)
    
    
    



    
    

    



