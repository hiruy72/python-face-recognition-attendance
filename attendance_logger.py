import sqlite3
import datetime

def init_db():
    conn = sqlite3.connect('database/attendance.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    time TEXT,
                    date TEXT)''')
    conn.commit()
    conn.close()

def mark_attendance(name):
    now = datetime.datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M:%S')

    # CSV logging
    with open('attendance.csv', 'a') as f:
        f.write(f'{name},{time_str},{date_str}\n')

    # SQLite logging
    conn = sqlite3.connect('database/attendance.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO attendance (name, time, date) VALUES (?, ?, ?)",
                (name, time_str, date_str))
    conn.commit()
    conn.close()
