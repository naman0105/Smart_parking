import sqlite3
import datetime
conn = sqlite3.connect('test.db')
print "Opened database successfully"
conn.execute('''CREATE TABLE PARKING
            (
             regNo        CHAR(20) PRIMARY KEY,
             entryTime    CHAR(20),
             exitTime     CHAR(20) NULL,
             charge       CHAR(20) NULL
             );
            ''')
print "Table created successfully"