import sqlite3

conn = sqlite3.connect('covid19.sqlite')
cur = conn.cursor()

print("Creating JSON output on covidData.js...")

cur.execute('SELECT month, COUNT(month) FROM cases GROUP BY month ORDER BY month ASC ')

fhand = open('covidData.js','w')
fhand.write('Months = [')

months = list()
for month in cur:
    months.append(month)

total = len(months) - 1
i=0
for month in months:
    if i< total:
        fhand.write('"' + month[0] + '", ')
    else:
        fhand.write('"' + month[0] + '"]\n\n')
    i = i + 1

fhand.write('Cases = {\n')

i=0
for element in months:
    month = element[0]
    fhand.write('"' + month + '":\n[\n')
    cur.execute('SELECT COUNT(*) FROM cases WHERE month = ?', ( month, ))
    total2 = cur.fetchone()
    cur.execute('SELECT s.code, s.name, c.fk_state_id, c.cases FROM cases c JOIN states s ON c.fk_state_id = id_state WHERE c.month = ?', ( month, ))
    j=0
    for item in cur:
        if j<total2[0] - 1:
            fhand.write('{"code":"'+ item[0] +'","name":"' + item[1] + '","cases":' + str(item[3]) + '},\n')
        else:
            fhand.write('{"code":"'+ item[0] +'","name":"' + item[1] + '","cases":' + str(item[3]) + '}\n')
        j = j + 1
    if i<total:
        fhand.write('],\n')
    else:
        fhand.write(']\n')
    i= i+1
fhand.write('}\n\n')

fhand.write('Deaths = {\n')

i=0
total = len(months) - 1
for element in months:
    month = element[0]
    fhand.write('"' + month + '":\n[\n')
    cur.execute('SELECT COUNT(*) FROM deaths WHERE month = ?', ( month, ))
    total2 = cur.fetchone()
    cur.execute('SELECT s.code, s.name, c.fk_state_id, c.deaths FROM deaths c JOIN states s ON c.fk_state_id = id_state WHERE c.month = ?', ( month, ))
    j=0
    for item in cur:
        if j<total2[0] - 1:
            fhand.write('{"code":"'+ item[0] +'","name":"' + item[1] + '","deaths":' + str(item[3]) + '},\n')
        else:
            fhand.write('{"code":"'+ item[0] +'","name":"' + item[1] + '","deaths":' + str(item[3]) + '}\n')
        j = j + 1
    if i<total:
        fhand.write('],\n')
    else:
        fhand.write(']\n')
    i= i+1
fhand.write('}\n\n')

fhand.write('Vaccines = {\n')

i=0
total = len(months) - 1
for element in months:
    month = element[0]
    fhand.write('"' + month + '":\n[\n')
    cur.execute('SELECT COUNT(*) FROM vaccines WHERE month = ?', ( month, ))
    total2 = cur.fetchone()
    cur.execute('SELECT s.code, s.name, c.fk_state_id, c.vaccines FROM vaccines c JOIN states s ON c.fk_state_id = id_state WHERE c.month = ?', ( month, ))
    j=0
    for item in cur:
        if j<total2[0] - 1:
            fhand.write('{"code":"'+ item[0] +'","name":"' + item[1] + '","vaccines":' + str(item[3]) + '},\n')
        else:
            fhand.write('{"code":"'+ item[0] +'","name":"' + item[1] + '","vaccines":' + str(item[3]) + '}\n')
        j = j + 1
    if i<total:
        fhand.write('],\n')
    else:
        fhand.write(']\n')
    i= i+1
fhand.write('}\n\n')


