from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_socketio import SocketIO
import sqlite3

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)

conn = sqlite3.connect('events.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS events
                  (id INTEGER PRIMARY KEY, date TEXT, time TEXT, event TEXT)''')
conn.commit()

@app.route('/')
def index():
    cursor.execute('SELECT * FROM events ORDER BY date, time')  # Добавлено ORDER BY для сортировки по дате и времени
    events = cursor.fetchall()
    return render_template('index.html', events=events)

@app.route('/add_event', methods=['POST'])
def add_event():
    date = request.form['date']
    event = request.form['event']
    time = request.form['time']
    cursor.execute('INSERT INTO events (date, time, event) VALUES (?, ?, ?)', (date, time, event))
    conn.commit()
    return redirect(url_for('index'))

@app.route('/delete_event', methods=['POST'])
def delete_event():
    date = request.form['date']
    time = request.form['time']
    cursor.execute('DELETE FROM events WHERE date=? AND time=?', (date, time))
    conn.commit()
    return redirect(url_for('index'))

@app.route('/get_event_data')
def get_event_data():
    cursor.execute('SELECT * FROM events ORDER BY date, time')  # Добавлено ORDER BY для сортировки по дате и времени
    events = cursor.fetchall()
    event_list = [{'date': event[1], 'time': event[2], 'event': event[3]} for event in events]
    return jsonify({'events': event_list})

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
