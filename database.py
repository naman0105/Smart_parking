import time
import sqlite3

chargePerUnitTime = 0.1

def checkExistance(conn, registration):
    cur = conn.cursor()
    cur.execute("SELECT * FROM PARKING WHERE regNo = ?" ,(registration,))
    rows = cur.fetchall()
    if(len(rows) == 0):
        return False
    else:
        return True



def Database_access(registration):
    #!/usr/bin/python

    conn = sqlite3.connect('test.db')
    print "Opened database successfully"
    starttime = str(time.time())

    if(checkExistance(conn, registration) == False):

        sql = '''INSERT INTO PARKING (regNo, entryTime) VALUES(?, ?)'''
        conn.execute(sql,(registration, starttime))

    else:

        cur = conn.cursor()
        cur.execute("SELECT entryTime FROM PARKING WHERE regNo = ?", (registration,))
        rows = cur.fetchall()
        starttime = rows[0][0]

        endTime = time.time()
        timeParked = endTime - float(starttime)
        charge = timeParked * chargePerUnitTime

        conn.execute("UPDATE PARKING SET exitTime= ?, charge= ? WHERE regNo = ?", (str(endTime), str(charge), str(registration)))
        #cur = conn.cursor()
        #cur.execute("SELECT * FROM PARKING")

    cur = conn.cursor()
    cur.execute("SELECT * FROM PARKING")
    rows = cur.fetchall()
    for row in rows:
        print(row)

    conn.commit()
    conn.close()

#Database_access("wewe9444")
